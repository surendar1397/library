from flask import Flask
from flask import render_template
import sqlite3

def create_db():
    db = sqlite3.connect("db.sqlite")
    table1 = "create table if not exists Books (title text, authors text, isbn text primary key, publisher text,page integer, total integer)"
    cur = db.cursor()
    cur.execute(table1)
    db.commit()

    table2 = "create table if not exists Members (name text, emailid text primary key, score integer)"
    cur.execute(table2)
    db.commit()

    table3 = "create table if not exists Transactions (txn_id text primary key,emailid text,isbn text,return_date text,returned_date text, fees integer)"
    cur.execute(table3)
    db.commit()


create_db()

app = Flask(__name__)

@app.route('/')
def api_tester():
    return render_template('index.html')

app.run(debug=True)
