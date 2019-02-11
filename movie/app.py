from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DB_DIR = os.path.join(BASE_DIR, "blog.db")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
db.init_app(app)


class Movie(db.Model):
    """Boxoffice Movie Information"""
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    title_en = db.Column(db.String, unique=True, nullable=False)
    audience = db.Column(db.Integer, nullable=False)
    open_date = db.Column(db.DateTime, nullable=False)
    genre = db.Column(db.String, nullable=False)
    watch_grade = db.Column(db.String, nullable=False)
    score = db.Column(db.Float, nullable=False)
    poster_url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)


db.create_all()

@app.route("/")
@app.route("/movies")
def index():
    """
    5. (선택) 추가적인 영화 정보가 표시됩니다.
    """
    return render_template("index.html", movies=Movie.query.all())

@app.route("/movies/new")
def new():
    return render_template("new.html")

@app.route("/movies/create", methods=["POST"])
def create():
    movie = Movie(
        title=request.form.get("title"),
        title_en=request.form.get("title_en"),
        audience=request.form.get("audience"),
        open_date=datetime.strptime(request.form.get("open_date"), "%Y-%m-%d"),
        genre=request.form.get("genre"),
        watch_grade=request.form.get("watch_grade"),
        score=request.form.get("score"),
        poster_url=request.form.get("poster_url"),
        description=request.form.get("description")
    )
    db.session.add(movie)
    db.session.commit()
    return redirect("/movies/{}".format(movie.id))

@app.route("/movies/<int:movie_id>")
def show(movie_id):
    """
    2. (필수) 영화 정보의 최하단에는 목록 , 수정 , 삭제 링크가 있으며, 클릭 시 각각 영화 목록 ,
        해당 영화 정보 수정 Form , 해당 영화 정보 삭제 페이지로 이동합니다
    """
    return render_template("show.html", movie=Movie.query.get(movie_id))

@app.route("/movies/<int:movie_id>/edit")
def edit(movie_id):
    """
    2. (필수) 해당 Primary Key를 가진 영화 정보를 수정할 수 있는 Form이 표시 되며, 이전 정보가 입력된 채
    로 표시됩니다.
    3. (필수) Form에 작성된 정보는 Submit 버튼 클릭 시 영화 정보 수정 페이지로 수정 요청(request)과
    함께 전송됩니다.
    4. (선택) 요청을 보내는 방식(method)은 GET, POST 중 어느 것을 사용하여도 무관합니다
    """
    return render_template("edit.html", movie=Movie.query.get(movie_id))

@app.route("/movies/<int:movie_id>/update", methods=["POST"])
def update(movie_id):
    movie = Movie.query.get(movie_id)
    movie.title=request.form.get("title")
    movie.title_en=request.form.get("title_en")
    movie.audience=request.form.get("audience")
    movie.open_date=datetime.strptime(request.form.get("open_date"), "%Y-%m-%d")
    movie.genre=request.form.get("genre")
    movie.watch_grade=request.form.get("watch_grade")
    movie.score=request.form.get("score")
    movie.poster_url=request.form.get("poster_url")
    movie.description=request.form.get("description")
    db.session.commit()
    return redirect("/movies/{}".format(movie_id))

@app.route("/movies/<int:movie_id>/delete")
def delete(movie_id):
    movie = Movie.query.get(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect("/movies")
    