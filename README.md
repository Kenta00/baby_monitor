# 赤ちゃんモニター

IOTを活用した物をグループで制作した際に作成したウェブアプリケーションです。
自分の担当分だったサーバー側のソースコードを公開しています。

画像や音声はインターネットのフリー素材を使用しています。

## 概要

赤ちゃんが泣いた時に、画面表示が切り替わって知らせるシステムです。
設定しておくと、メールで知らせてくれます。

## 各種ページ

/　トップページ
/top　トップページ
/check　赤ちゃんモニターページ
/option　設定ページ
/health　健康管理ページ（見た目だけ）

## 環境

Windows 10、python 3.8.5で動作確認しています。

Flaskのインストール
''pip install Flask''

Flask Mailのインストール
''pip install Flask-Mail''

## 使い方

baby_monitor.pyを実行すると、サーバーが起動します。
ハードウェアから　(url)/getadc?BABY=　というリクエストが来ると、BABYの値を取得します。
ハードウェアでは、一定以上の騒音が検知されると、BABY=1を、それ以外の時はBABY=0を送信するようになっていました。
トップページに戻った瞬間にBABYの値は０にリセットされます。

実際にメールを送信するには、baby_mail.pyの以下の部分(4~11行目)を書き換えてください。
''
#mail settings
#app.config['MAIL_SERVER']=''
#app.config['MAIL_PORT'] = 
#app.config['MAIL_USERNAME'] = ''
#app.config['MAIL_PASSWORD'] = ''
#app.config['MAIL_USE_TLS'] = 
#app.config['MAIL_USE_SSL'] = 
#app.config['MAIL_DEFAULT_SENDER']=''
''


赤ちゃんモニター（/check）のページを開いておくと、赤ちゃんが泣いた場合は、画面が切り替わります。

赤ちゃんの名前やメール受信設定は、設定ページ（/option）で行います。
現段階では生年月日は、特に意味はありません。

## 備考

PCで見る想定しかしていなかったので、スマホで見るとレイアウトが崩れます。
気が向いたらレスポンシブ対応します。

