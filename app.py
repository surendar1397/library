from flask import Flask
from flask import render_template, request
import sqlite3, traceback

def create_db():
    table1 = "create table if not exists Books (title text, author text, isbn text primary key, publisher text,page integer, total integer)"
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

@app.route('/new_book')
def new_book():
    return render_template('add_book.html')

@app.route('/add_book', methods = ['post'])
def update_book_in_db():
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    publisher = request.form.get('publisher')
    page = request.form.get('page')
    quantity = request.form.get('qty')
    try:
        query = f"insert into books values ('{title}','{author}','{isbn}','{publisher}','{page}','{quantity}')"
        cur.execute(query)
    except:
        error = "updation failed for the book "+title
        return render_template('status.html',message = error)
    else:
        message = "book is updated"
        db.commit()
        return render_template('status.html',message = message)
    finally:
        cur.close()
        db.close()

@app.route('/search_book')
def search_book():
    return render_template('lend_book.html')

@app.route('/lend_book',methods = ['post'])
def book_enquiry_in_db():
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()
    title = request.form.get('title')
    try:
        query = f"select title, total from Books where title like '%{title}%'"
        rows = cur.execute(query)
        rows =[ (i,j) for i,j in rows.fetchall() ]
    except:
        msg = traceback.format_exc()
        error = "The book menioned is not available"+msg
        return render_template('status.html',message = error)
    else:
        message = str(rows)
        db.commit()
        return render_template('status.html',message = message)
    finally:
        cur.close()
        db.close()

@app.route('/update_score')
def update_score_page():
    return render_template('update_score.html')

@app.route('/member_score', methods=['post'])
def change_score():
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()
    email = request.form.get('email')
    score = request.form.get('score')
    try:
        query = f"select * from Members where emailid='{email}'"
        rows = cur.execute(query)
        rows = rows.fetchall()
        if rows:
            q2 = f"update Members set score={score} where emailid='{email}'"
            cur.execute(q2)
        else:
            return render_template('status.html', message='No such member')
    except:
        msg = traceback.format_exc()
        return render_template('status.html',message = msg)
    else:
        message = str(rows)
        db.commit()
        return render_template('status.html',message = message)
    finally:
        cur.close()
        db.close()

@app.route('/delete_member')
def delete_member_page():
    return render_template('remove_member.html')

@app.route('/remove_member', methods=['post'])
def delete_member():
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()
    email = request.form.get('email')
    try:
        query = f"select * from Members where emailid='{email}'"
        rows = cur.execute(query)
        rows = rows.fetchall()
        if rows:
            q2 = f"delete from Members where emailid='{email}'"
            cur.execute(q2)
        else:
            return render_template('status.html', message='No such member')
    except:
        msg = traceback.format_exc()
        return render_template('status.html',message = msg)
    else:
        message = str(rows)
        db.commit()
        return render_template('status.html',message = message)
    finally:
        cur.close()
        db.close()


app.run(debug=True)
