from flask import Flask, send_file, render_template
from datetime import datetime
from bs4 import BeautifulSoup as bs

import random
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/name")
def name():
    return "JAESEO LEE"
    
@app.route("/hello/<name>")
def hi(name):
    return "hello {name}".format(name=name)
    
@app.route("/cube/<num>")
def cube(num):
    return str(float(num)**3)

@app.route("/reverse/<string>")
def reverse(string):
    return string[::-1]
    
@app.route("/palindrome/<string>")
def palindrome(string):
    str_len = len(string)
    if str_len%2==1:
        str1 = string[:str_len//2]
        str2 = string[-1:str_len//2:-1]
    else:
        str1 = string[:str_len//2]
        str2 = string[str_len//2::-1]
    if str1==str2:
        return "True"
    else:
        return "False"
        
@app.route("/profile")
def profile():
    return send_file('profile.html')
    
@app.route("/lotto")
def lotto():
    result = str(sorted(random.sample(range(1, 46), 6)))
    return render_template("lotto.html", lotto=result)
    
@app.route("/kos")
def kos():
    sise_url = "https://finance.naver.com/sise/"
    response = requests.get(sise_url)
    doc = bs(response.text, 'html.parser')
    kospi = doc.select_one("#KOSPI_now").text
    kosdaq = doc.select_one("#KOSDAQ_now").text
    return render_template("kospi.html", now_dt=datetime.now(), kospi=kospi, kosdaq=kosdaq)
    
@app.route("/newyear")
def newyear():
    today = datetime.strftime(datetime.now(), "%m%d")
    isnyd = True if today=="0101" else False
    return render_template("newyear.html", isnyd=isnyd)
    
@