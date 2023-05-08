from flask import Flask,request,jsonify,render_template,redirect
from flask_mail import Mail, Message
app = Flask(__name__, static_folder='./templates/src')
# mail settings
#app.config['MAIL_SERVER']=''
#app.config['MAIL_PORT'] = 
#app.config['MAIL_USERNAME'] = ''
#app.config['MAIL_PASSWORD'] = ''
#app.config['MAIL_USE_TLS'] = 
#app.config['MAIL_USE_SSL'] = 
#app.config['MAIL_DEFAULT_SENDER']=''
mail = Mail(app)
# top page
@app.route("/",methods=['GET','POST'])
def login():
    global baby_name
    global email_valid
    global email
    global mode
    global adc_value
    adc_value = 0
    mode = 'sleep'
    baby_name = 'あか'
    email_valid = 0
    email=""
    if request.method == 'POST':
        return do_login()
    else:
        return render_template('index.html',login=1)
def do_login():
    global user_name
    user_name = request.form['user_name']
    password = request.form['password']
    # password example
    if user_name != 'ママ' or password != 'aka':
        return render_template('index.html', error_message='ユーザー名かパスワードが間違っています',login = 1)
    return redirect('/top')
@app.route("/top",methods=['GET'])
def top():
    global mode
    global adc_value
    global user_name
    global baby_name
    adc_value = 0
    mode = 'sleep'
    return render_template('index.html',login = 0, user_name=user_name,baby_name=baby_name)
# adc request
@app.route("/getadc",methods=['GET'])
def getadc():
    global adc_value
    global mode
    global email_valid
    print( "Request = {}".format( request.args ) )
    adc_value=request.args.get('BABY', type=int)
    print(email_valid)
    if adc_value == 1:
        if mode=='sleep' and email_valid == 1:
            email_valid=2
        print( "BABY is crying" )
        mode = 'cry'
    elif adc_value == 0:
        print( "BABY is sleeping" )
    else:
        print( "Error_BABY={}".format(adc_value) )
    if email_valid == 2:
        return send_email()
    else:
        return jsonify( adc=adc_value)
def send_email():
    global email
    global email_valid
    global user_name
    global baby_name
    msg = Message(baby_name + 'ちゃんが泣いています', recipients=[email])
    msg.body = user_name+"様\n"+baby_name+"ちゃんが泣いています。"
    mail.send(msg)
    email_valid=1
    return jsonify( adc=adc_value)
# monitor page
@app.route("/check",methods=['GET','POST'])
def check():
    global adc_value
    if adc_value == 1:
        return render_template('check.html', adc_value=adc_value, mode=mode)
    elif adc_value ==0:
        return status()
    else:
        return "Error_BABY={}".format(adc_value)
def status():
    global mode
    if mode != 'cry' and mode != 'sleep':
        print("mode error")
        return "Error_mode={}".format(mode)
    else :
        return render_template('check.html', adc_value=adc_value, mode=mode)
# health page
@app.route("/health",methods=['GET','POST'])
def health():
    return render_template('health.html')
# option page
@app.route("/option", methods=['GET', 'POST'])
def option():
    global baby_name
    global email_valid
    global email
    if request.method == 'POST':
        return option_change()
    else:
        return render_template('option.html', baby_name=baby_name, email_valid=email_valid,email=email)
def option_change():
    global baby_name
    global email_valid
    global email
    baby_name = request.form['baby_name']
    email_valid = int(request.form.get('email_valid','0'))
    email = request.form['email']
    year = request.form.get("year")
    month = request.form.get("month")
    day = request.form.get("day")
    return redirect('/top')
# error page
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404
@app.errorhandler(500)
def server_error(error):
    return render_template('error.html'), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000, debug=False)
