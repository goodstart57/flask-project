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
        """query in python sqlite3
        :args:
            q_type (str) -- ["select_all", "select", "create", "update", "delete"]
            t_name (str) -- table name
        
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
            