import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)

DATABASE = 'names.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_table():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        db.commit()

create_table()

@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM names")
    names = cursor.fetchall()
    return render_template('index.html', names=names)

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO names (name) VALUES (?)", (name,))
    db.commit()
    return render_template('greet.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
