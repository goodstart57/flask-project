from flask import Flask, render_template, request
from faker import Faker

from datetime import datetime

import random
import csv

app = Flask(__name__)
fake = Faker('ko_KR')

visited_user_job = {}

with open('fish.csv', 'r', encoding='utf-8') as f:
    fish = {}
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        fish[(row[0], row[1])] = row[2]

# '/' :  사용자의 이름을 입력 받습니다.
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/match')
def match():
    me = request.args.get('me')
    you = request.args.get('you')
    try:
        rate = fish[(me, you)]
    except:
        rate = random.randint(50, 100)
        fish[(me, you)] = rate
        with open('./fish.csv', 'a', encoding='utf-8') as f:
            fishwriter = csv.writer(f)
            fishwriter.writerow([me, you, rate])
    return render_template('match.html', me=me, you=you, rate=rate)
    
@app.route('/admin')
def admin():
    return render_template('admin.html', fishes=fish.items())
    
# '/pastlife' : 사용자의 (랜덤으로 생성된) 전생/직업을 보여준다.
@app.route('/pastlife')
def pastlife():
    user_name = request.args.get('name')
    try:
        past_job = visited_user_job[user_name]
    except:
        past_job = fake.job()
        visited_user_job[user_name] = past_job
    return render_template('pastlife.html', pjob=past_job, name=user_name)

# @app.route('/pastlife')
# def pastlife():
#     user_name = request.args.get('name')
#     seed_num = datetime.now().day
#     for char in user_name: seed_num+=ord(char)
#     seed_num = str(seed_num)
#     past_job = fake.seed_instance(seed_num).job()
#     return render_template('pastlife.html', pjob=past_job, name=user_name)