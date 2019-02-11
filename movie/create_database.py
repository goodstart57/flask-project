from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import xlrd
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
db.init_app(app)

# create movies table (original)
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


# insert data (original)
wb = xlrd.open_workbook("static/data/data.xlsx")
sheet = wb.sheet_by_index(0)
for i in range(1, sheet.nrows):
    row = sheet.row_values(i)
    db.session.add(Movie(
        title=row[0],
        title_en=row[1],
        audience=row[2],
        open_date=datetime.strptime(str(int(row[3])), "%Y%m%d"),
        genre=row[4],
        watch_grade=row[5],
        score=row[6],
        poster_url=row[7],
        description=row[8]
    ))
db.session.commit()


# ## create movies table
# class Movie(db.Model):
#     """Boxoffice Movie Information"""
#     __tablename__ = "movies"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.String, unique=True, nullable=False)
#     title_en = db.Column(db.String, unique=True, nullable=False)
#     audience = db.Column(db.Integer, nullable=False)
#     show_time = db.Column(db.Integer, nullable=False)
#     open_date = db.Column(db.DateTime, nullable=False)
#     genre = db.Column(db.String, nullable=False)
#     watch_grade = db.Column(db.String, nullable=False)
#     score = db.Column(db.Float, nullable=False)
#     actor = db.Column(db.String, nullable=False)
#     nation = db.Column(db.String, nullable=False)
#     distributor = db.Column(db.String, nullable=False)
#     poster_url = db.Column(db.Text, nullable=False)
#     review_url = db.Column(db.Text, nullabel=False)
#     description = db.Column(db.Text, nullable=False)

# db.create_all()

# ## insert my data
# with open("static/data/my_data.csv", "r") as f:
#     movies = f.readlines()
#     movies = list(map(lambda x: x.split(","), movies[1:]))
#     for movie in movies:
#         row = sheet.row_values(i)
#         db.session.add(Movie(
#             title=movie[1],
#             title_en=movie[17],
#             audience=movie[0],
#             show_time=movie[23],
#             open_date=movie[3],
#             genre=movie[14],
#             watch_grade=movie[15],
#             score=movie[7],
#             actor=movie[9],
#             nation=movie[19],
#             distributor=movie[13],
#             poster_url=movie[6],
#             review_url=movie[8],
#             description=movie[]
#         ))
#     db.session.commit()
