from flask import Flask, render_template, request, redirect
from db_controller import DbController

import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "assets\\data")
QUESTION_DB_DIR = os.path.join(BASE_DIR, "question_db.txt")

@app.route("/")
def index():
    """사용자의 질문 받는다."""
    dbc = DbController("board.sqlite3")
    articles = dbc.query(q_type="select_all", t_name="articles")
    items = {"articles": articles}
    return render_template("index.html", items=items)
    
@app.route("/create", methods=["POST"])
def create():
    dbc = DbController("board.sqlite3")
    dbc.query(
        q_type="insert",
        t_name="articles",
        condition=None,
        title=request.form.get("title"),
        content=request.form.get("content")
    )
    return redirect("/")
    
@app.route("/delete/<int:article_id>")
def delete(article_id):
    dbc = DbController("board.sqlite3")
    dbc.query(
        q_type="delete",
        t_name="articles",
        condition="id={}".format(article_id)
    )
    return redirect("/")
    
@app.route("/edit/<int:article_id>")
def edit(article_id):
    dbc = DbController("board.sqlite3")
    data = dbc.query(
        q_type="select_one",
        t_name="articles",
        condition="id={}".format(article_id),
        n=1
    )
    article_info = {"id": data[0], "title": data[1], "content": data[2]}
    return render_template("edit.html", article_info=article_info)

@app.route("/update/<int:article_id>", methods=["POST"])
def update(article_id):
    dbc = DbController("board.sqlite3")
    dbc.query(
        q_type="update",
        t_name="articles",
        condition="id={}".format(article_id),
        title=request.form.get("title"),
        content=request.form.get("content")
    )
    return redirect("/")
