from flask import Flask, render_template, request

import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "assets\\data")
QUESTION_DB_DIR = os.path.join(BASE_DIR, "question_db.txt")

@app.route("/")
def index():
    """사용자의 질문 받는다."""
    return render_template("index.html")
    
@app.route("/ask")
def ask():
    """
    사용자의 질문을 보여주고,
    <h1>성공적으로 질문이 작성되었습니다.</h1>
    quest.txt라는 파일에 질문을 저장한다.
    """
    question = request.args.get("question")
    with open(QUESTION_DB_DIR, "a") as f:
        f.write(question + "\n")
    return render_template("ask.html", question=question)

@app.route("/admin")
def admin():
    """지금까지 쌓인 질문을 모두 보여준다."""
    with open(QUESTION_DB_DIR, "r") as f:
        questions = list(map(lambda x: x.strip("\n"), f.readlines()))
    return render_template("admin.html", questions=questions)
    
@app.route("/admin/remove")
def remove():
    """원하는 것 삭제"""
    rq = request.args.get("rq") + "\n"
    with open(QUESTION_DB_DIR, "r") as of:
        ori_lines = of.readlines()
        new_lines = [word for word in ori_lines if word != rq]
    with open(QUESTION_DB_DIR, "w") as nf:
        nf.writelines(new_lines)
    return render_template("admin.html", questions=new_lines)