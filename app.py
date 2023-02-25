from flask import Flask
from flask import render_template, request
import sqlite3, traceback

def create_db():
    table1 = "create table if not exists Books (title text, authors text, isbn text primary key, publisher text,page integer, total integer)"
    db = sqlite3.connect("db.sqlite")
    cur = db.cursor()
    cur.execute(table1)
    db.commit()

    table2 = "create table if not exists Members (name text, emailid text primary key, score integer)"
    cur.execute(table2)
    db.commit()

    table3 = "create table if not exists Transactions (txn_id text primary key,emailid text,isbn text,return_date text,returned_date text, fees integer)"
    cur.execute(table3)
    db.commit()
    cur.close()
    db.close()


create_db()

app = Flask(__name__)

@app.route('/')
def api_tester():
    return render_template('index.html')

@app.route('/new_member')
def new_member():
    return render_template('add_member.html')

@app.route('/add_member',methods=['POST'])
def update_member_in_db():
    db = sqlite3.connect("db.sqlite")
    cur = db.cursor()
    email = request.form.get('emailid')
    name = request.form.get('name')
    try:
        query = f"insert into Members values ('{name}', '{email}', 4)"
        cur.execute(query)
    except:
        # error = traceback.format_exc()
        error = "Member Creation Failed for "+email
        return render_template('status.html', message=error)
    else:
        message = "Member Created"
        db.commit()
        return render_template('status.html', message=message)
    finally:
        cur.close()
        db.close()

app.run(debug=True)
