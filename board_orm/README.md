# 블로그 만들기

## 0. 프로젝트 디렉토리 구조

```
blog
  ├─ static
        └─ assets
             └─ style.css
  ├─ templates
       ├─ base.html
       ├─ edit.html
       ├─ index.html
       ├─ new.html
       └─ read.html
  ├─ app.py
  ├─ blog.db
  ├─ db_controller.py
  └─ README.md
```



## 1. Database 구축

### Database 생성

`blog.db` 라는 이름의 database를 만들기 위해서 bash 창에서 아래 명령어를 실행합니다.

```bash
$ sqlite3 blog.db
```

위 명령어를 통해 sqlite 콘솔창에 들어갈 수 있는데 여기서 아래 명령어를 통해서 sqlite3 데이터베이스를 파일로 저장할 수 있습니다.

```sqlite
.database
```

```
seq  name             file                                                      
---  ---------------  ----------------------------------------------------------
0    main             /home/ubuntu/workspace/blog/blog.db  
```



### articles 테이블 생성

```sqlite
-- init_db.sql
CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    created_at TEXT,
    author TEXT
);
```

위 파일을 생성하고 blog.db 콘솔 내에서 아래 명령어를 통해 `articles` 테이블을 생성합니다.

```sqlite
.read init_db.sql articles
.tables
.schema articles
```

```
articles
CREATE TABLE articles (
	id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    created_at TEXT,
    author TEXT
);
```



### flask 프로젝트에 database 경로 설정

```python
# app.py
from flask import Flask, render_template, request, redirect
from db_controller import DbController
from datetime import datetime

import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DB_DIR = os.path.join(BASE_DIR, "blog.db")
```



## 2. 각 페이지 생성

### 글 목록

```python
# app.py
@app.route("/")
@app.route("/articles")
def index():
    dbc = DbController("blog.db")
    articles = dbc.query(q_type="select_all", t_name="articles")
    items = {"articles": articles}
    return render_template("index.html", items=items)
```

- 첫 화면으로 글 목록을 사용할 예정이기 때문에 `/`와 `/articles` 모두 index.html로 routing 합니다.
- sqlite에 sql문을 쿼리하는 것은 전에 만들어 두었던 `DbController` 클래스를 이용하여 수행합니다. (DbController는 blog를 만드는 것과 관계 없으므로 README 하단에 첨부하겠습니다.)



### 새 글 생성

```python
@app.route("/articles/new")
def create():
    return render_template("new.html")
    
@app.route("/articles/create", methods=["POST"])
def create_article():
    dbc = DbController("blog.db")
    created_at = datetime.now().strftime("%Y/%m/%d %H:%M")
    dbc.query(
        q_type="insert",
        t_name="articles",
        condition=None,
        title=request.form.get("title"),
        content=request.form.get("content"),
        author=request.form.get("author"),
        created_at=created_at
    )
    article_id = dbc.query(
        q_type="select_one",
        t_name="articles",
        condition="title='{}' AND content='{}' AND author='{}' AND created_at='{}'".format(request.form.get("title"), request.form.get("content"), request.form.get("author"), created_at),
        n=1
    )[0]
    return redirect("/articles/{}".format(article_id))
```

- 첫 화면에서 `게시글 작성하기`를 누르면 `/articles/new`로 라우팅되어 `new.html`로 접근하여 새 글 생성폼으로 이동합니다. 

- `new.html`에서 `author`, `title`, `content`를 입력하고 `게시글 작성하기`를 누르면 `/articles/create`로 post  request가 전송되어 `blog.db`의 `articles`테이블에 새로운 행을 입력합니다.

- 입력된 데이터를 기반으로 다시 id를 조회하고, id를 이용하여 글 상세 페이지인 `/articles/<int:article_id>`로 라우팅 합니다.

- `created_at`의 경우 python의 datetime을 활용하여 작성 시간을 `%Y/%m/%d %H:%M` 문자열 포맷으로 저장합니다.



### 글 상세 페이지

```python
@app.route("/articles/<int:article_id>")
def read_article(article_id):
    dbc = DbController("blog.db")
    this_article_info = dbc.query(
        q_type="select_one",
        t_name="articles",
        condition="id={}".format(article_id),
        n=1
    )
    return render_template("read.html", article_info=this_article_info)
```

- 첫 화면에서 게시글 제목을 누르는 등 글 상세 페이지로 이동하려 하는 경우 `/articles/<int:article_id>`으로 라우팅되어 articles 뒤의 경로인 article_id가 `read_article` 함수에서 정수형 변수로 사용가능합니다.

- 이를 통해서 id로 `blog.db`를 쿼리하여 게시글 상세 페이지에서 게시글의 정보를 볼 수 있습니다.



### 글 수정

```python
@app.route("/articles/<int:article_id>/edit")
def edit(article_id):
    dbc = DbController("blog.db")
    this_article_info = dbc.query(
        q_type="select_one",
        t_name="articles",
        condition="id={}".format(article_id),
        n=1
    )
    return render_template("edit.html", article_info=this_article_info)

@app.route("/articles/<int:article_id>/update", methods=["POST"])
def update_article(article_id):
    dbc = DbController("blog.db")
    this_article_info = dbc.query(
        q_type="update",
        t_name="articles",
        condition="id={}".format(article_id),
        title=request.form.get("title"),
        content=request.form.get("content"),
        author=request.form.get("author"),
        created_at=datetime.now().strftime("%Y/%m/%d %H:%M")
    )
    return redirect("/articles/{}".format(article_id))
```

- 글 상세보기 페이지에서 `수정`버튼을 누르는 경우 `/articles/<int:article_id>/edit`으로 라우팅되어 `edit.html`페이지로 연결됩니다.

- 이때 `article_id`를 사용하여 `blog.db`에 저장되어있는 게시글 정보를 불러와서 edit from에 미리 로드되도록 설정합니다.

- `edit.html`내에서 `title, content, author`란을 수정한 후 `게시글 수정하기`를 누르면 `/articles/<int:article_id>/update`로 라우팅되어 변경된 사항이 데이터베이스에 반영됩니다.

- 그 후, 글 상세보기 페이지로 이동합니다.



### 글 삭제

```python
@app.route("/articles/<int:article_id>/delete", methods=["POST"])
def delete_article(article_id):
    dbc = DbController("blog.db")
    this_article_info = dbc.query(
        q_type="delete",
        t_name="articles",
        condition="id={}".format(article_id)
    )
    return redirect("/articles")
```

- 글 상세보기 페이지에서 `삭제`버튼을 누르는 경우 `/articles/<int:article_id>/delete`로 라우팅되어 `blog.db`에서 `article_id`와 같은 id를 조회하여 데이터 베이스 상의 데이터를 삭제합니다.

- 그 후, 글 목록 페이지로 이동합니다.



## 3. DbController

```python
import sqlite3

class DbController:
    def __init__(self, db_name):
        self.c = sqlite3.connect(db_name)
        self.db = self.c.cursor()
    
    def __delf__(self):
        self.c.close()
        
    def _strf(self, x):
        if isinstance(x, str):
            return "'{}'".format(x)
        else:
            return x
    
    def _create(self, t_name, kwargs):
        sql = "CREATE TABLE {} (id PRIMARY KEY AUTOINCREMENT,"
        for item in kwargs.items():
            sql = "{} {} {},".format(sql, item[0], item[1])
        sql = sql[:-1] + ")"
        self.db.execute(sql)
        self.c.commit()
        
    def _insert(self, t_name, kwargs):
        cols, vals = "(", "("
        for item in kwargs.items():
            cols = "{} {},".format(cols, item[0])
            vals = "{} {},".format(vals, self._strf(item[1]))
        cols, vals = cols[:-1] + ")", vals[:-1] + ")"
        sql = "INSERT INTO {} {} VALUES {}".format(t_name, cols, vals)
        print(sql)
        self.db.execute(sql)
        self.c.commit()
    
    def _select(self, t_name, condition, n="all"):
        sql = "SELECT * FROM {}".format(t_name)
        if condition is not None:
            sql = sql + " WHERE {}".format(condition)
        if n == 1 or n == '1':
            self.db.execute(sql)
            return self.db.fetchone()
        elif n is not "all":
            sql = sql + " LIMIT {}".format(n)
        self.db.execute(sql)
        return self.db.fetchall()
        
    def _update(self, t_name, condition, kwargs):
        kv = ", ".join(map(lambda x: "{}={}".format(x[0], self._strf(x[1])), kwargs.items()))
        if condition is None:
            sql = "UPDATE {} SET {}".format(t_name, kv)
        else:
            sql = "UPDATE {} SET {} WHERE {}".format(t_name, kv, condition)
        self.db.execute(sql)
        self.c.commit()
    
    def _delete(self, t_name, condition):
        sql = "DELETE FROM {} WHERE {}".format(t_name, condition)
        self.db.execute(sql)
        self.c.commit()
    
    def query(self, q_type, t_name="articles", condition=None, **kwargs):
        if q_type == "select_all":
            return self._select(t_name, condition, n="all")
        if q_type == "select_one":
            return self._select(t_name, condition, n=1)
        elif q_type == "select":
            return self._select(t_name, condition, n=kwargs["n"])
        elif q_type == "create":
            self._create(t_name, kwargs)
        elif q_type == "insert":
            self._insert(t_name, kwargs)
        elif q_type == "update":
            self._update(t_name, condition, kwargs)
        elif q_type == "delete":
            self._delete(t_name, condition=condition)
        else:
            print("enter the correct input")      
```



생성자로 sqlite3 database의 경로(파일명 포함)를 받으면 sqlite3 패키지를 이용하여 database를 읽어들어와서 sql 쿼리문을 작성하는 대신 python 함수로 database를 조작할 수 있는 클래스입니다.

`DbController`클래스의 인스턴스를 생성한 후 `query`메소드의 docstring으로 사용 예시를 볼 수 있으며 다음과 같습니다.

```python
"""query in python sqlite3
:args:
    q_type (str) -- ["select_all", "select", "create", "update", "delete"]
    t_name (str) -- table name
    condition (str) -- query condition
    *kwargs -- used to insert, update

:return:
    query result
    
:example:
    dbc = DbController("board.sqlite3")
    # select all
    dbc.query(q_type="select_all", t_name="articles", condition=None)
    # select 1
    dbc.query(q_type="select_one", t_name="articles", condition=None, n=1)
    # select n
    dbc.query(q_type="select", t_name="articles", condition=None, n=1)
    # create table
    dbc.query(q_type="create", t_name="articles", condition=None, title="TEXT", content="TEXT")
    # insert row
    dbc.query(q_type="insert", t_name="articles", condition=None, title="test dbc", content="test dbc")
    # update
    dbc.query(q_type="update", t_name="articles", condition="id=5", title="hi", content="wowowowowowow")
    dbc.query(q_type="select_all", t_name="articles", condition="id=5")
    # delete
    dbc.query(q_type="delete", t_name="articles", condition="id=5")
    dbc.query(q_type="select_all", t_name="articles", condition="id=5")
"""
```



### DbController 인스턴스 생성

```python
from db_controller import DbController

dbc = DbController("blog.db")
```



### blog.db의 모든 데이터 조회

```python
dbc.query(q_type="select_all", t_name="articles", condition=None)
```



### blog.db에서 title이 hi인 데이터 조회

```python
dbc.query(q_type="select_all", t_name="articles", condition="title='hi'")
```



### blog.db에서 새로운 레코드 생성

```python
dbc.query(q_type="insert", t_name="articles", condition=None, title="hi", content="hi everyone", author="goodstart57@gmail.com")
```



### blog.db에서 특정 레코드 제거

```python
dbc.query(q_type="delete", t_name="articles", condition="title='hi'")
```

