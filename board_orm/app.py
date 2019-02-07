from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DB_DIR = os.path.join(BASE_DIR, "blog.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
db.init_app(app)


class Article(db.Model):
    """
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
    );
    """
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False)


db.create_all()


@app.route("/")
@app.route("/articles")
def index():
    return render_template("index.html", articles=Article.query.all())
    
@app.route("/articles/new")
def create():
    return render_template("new.html")
    
@app.route("/articles/create", methods=["POST"])
def create_article():
    article = Article(
        title=request.form.get("title"),
        content=request.form.get("content"),
        author=request.form.get("author"),
        created_at=datetime.now().strftime("%Y/%m/%d %H:%M"),
    )
    db.session.add(article)
    db.session.commit()
    return redirect("/articles/{}".format(article.id))

@app.route("/articles/<int:article_id>")
def read_article(article_id):
    return render_template("read.html", article=Article.query.get(article_id))
    
@app.route("/articles/<int:article_id>/edit")
def edit(article_id):
    return render_template("edit.html", article=Article.query.get(article_id))

@app.route("/articles/<int:article_id>/update", methods=["POST"])
def update_article(article_id):
    article = Article.query.get(article_id)
    article.title = request.form.get("title")
    article.content = request.form.get("content")
    article.author = request.form.get("author")
    article.created_at = datetime.now().strftime("%Y/%m/%d %H:%M")
    db.session.commit()
    return redirect("/articles/{}".format(article.id))

@app.route("/articles/<int:article_id>/delete", methods=["POST"])
def delete_article(article_id):
    article = Article.query.get(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect("/articles")
