import sqlite3

c = sqlite3.connect("board.sqlite3")
db = c.cursor()

sql = """
CREATE TABLE articles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    content TEXT
);
"""
db.execute(sql)
c.commit()
c.close()