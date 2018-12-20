from flask import Flask, render_template, request

import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/sendmsg')
def sendmsg():
    text = request.args.get('msg')
    tele_chatbot_key = "<key>"
    method = "sendMessage"
    user_id = "<id>"
    # original_url = "https://api.telegram.org/"
    url = "https://api.hphk.io/telegram/bot{0}/{1}?chat_id={2}&text={3}".format(tele_chatbot_key, method, user_id, text)
    response = requests.get(url)
    return render_template('sendmsg.html', msg=text)
