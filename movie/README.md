

# 04 Project : CRUD

## 0. 프로젝트 작업 디렉토리

```
04_crud
  ├─static
      ├─data
          └─data.xlsx
      ├─css
          └─style.css
      ├─image
          ├─movie-header.jpg
          └─request-new-minfo.jpg
      ├─svg
          └─si-hlyph-button-plus.svg
  ├─templates
      ├─base.html
      ├─edit.html
      ├─index.html
      ├─layout.html
      ├─new.html
      └─show.html
  ├─app.py
  ├─create_database.py
  ├─movie.db
  └─README.md

```



## 1. 데이터베이스 생성

### flask-sqlalchemy를 이용한 sql query

#### create table

```sqlite
-- sqlite3
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
);
```

```python
# flask-sqlalchemy in python
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
db.create_all()
```

#### insert record

```sqlite
-- sqlite3
INSERT INTO articles (title, content) VALUES ('hi', 'im jaeseo');
```

```python
# flask-sqlalchemy in python
db.session.add(Article(
    title="hi",
    content="im jaeseo"
))
db.session.commit()
```

database에서는 트랜잭션을 끝내고 변경사항을 데이터베이스에 반영시키기 위해서 commit을 해줘야 합니다.



### 프로젝트에 적용

#### Configure flask-sqlalchemy

```python
# create_database.py : configure
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
```

`flask-sqlalchemy` 패키지를 이용하여 sqlite3 데이터베이스를 구축하기 위해서 환경을 설정합니다.

#### Create table

```python
# create_database.py : create table
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
```

명세와 같이 `Movie`클래스로 모델을 만들어 `movies`로 테이블명으로 이름을 정해줍니다.

#### Insert record(data)

```python
# create_database.py : insert data
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
```

데이터 전처리가 아닌 단순 불러오기라서 `pandas`보다 경량의 `xlrd`패키지를 이용하여 주어진 데이터 `data.xlsx`를 불러와서 각 행별로 데이터를 입력합니다.



## 2. Flask 프로젝트 생성

```python
# app.py
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
```

`flask-sqlalchemy`와 `movies`테이블을 만드는 작업을 예기치 못한 상황을 위해서 설정해 둡니다.



## 상세 페이지

### 영화 목록

![index](static\image\movie-index.png)

```python
# app.py : index
@app.route("/")
@app.route("/movies")
def index():
    return render_template("index.html", movies=Movie.query.all())
```

홈페이지 겸 영화 목록 페이지입니다.

- 도메인으로 직접 접근하는 사용자를 위해서 지정된 `/movies`경로 뿐만 아니라 root 경로도 라우팅해줍니다.
- `layout.html`로 `navbar`를 만들어 홈페이지로 접근할 수 있는 버튼을 만들고, 추후 추가될 인기 영화, 분류별 영화, 영화 검색 버튼을 추가했습니다.
- `base.html`은 `layout.html`을 상속받아서 `navbar`와 `header`를 가지고 있습니다.
- 영화 목록은 수평 스크롤로 구성되어 있습니다.
- 영화 목록의 좌측에서 새로운 영화를 등록할 수 있습니다.
- 영화 목록의 각 포스터를 누르면 영화 상세보기 페이지로 접근할 수 있습니다.



### 새 영화 등록

![new-movie](static\image\movie-new.png)

```python
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
```

`flask-sqlalchemy`에서 새로운 데이터 레코드를 입력하는 방법은 데이터베이스를 구축할 때 다뤘으므로 생략하겠습니다.

- 새 영화를 게시할 수 있는 `new.html`은 명세에 맞게 text, number, date 등으로 구성되어 있습니다.
- 평점을 입력하기 위해서 `input`의 `range` 타입을 사용했으며 0.5점 단위로 입력 가능합니다.
- `게시글 작성하기`를 누르면 작성된 영화 상세보기 페이지로 이동됩니다.



### 상세보기

![movie-show](static\image\movie-show.png)

```python
@app.route("/movies/<int:movie_id>")
def show(movie_id):
    return render_template("show.html", movie=Movie.query.get(movie_id))
```

`게시글 작성하기`를 통해서 상세보기 페이지로 이동한 화면입니다.

- url을 통해서 받은 movie객체의 movie_id를 이용하여 `movie.db`데이터베이스에서 영화정보를 쿼리하여 상세보기 페이지에 보여줍니다.
- 영화 한글 이름, 영화 영어 이름, 누적 관객수, 개봉 일자, 평점, 장르, 관람 등급, 영화 설명, 영화 포스터가 등록되어 있습니다.
- `delete`, `edit`, `go to list`기능을 수행할 수 있는 버튼이 있습니다.
- `edit`과 `delete`기능은 조회된 영화의 id를 기준으로 작동합니다.



### 수정하기

```python

```

