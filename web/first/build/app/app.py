import os
import sqlite3
import traceback
import random
import io
import sys
import time
from flask import Flask, abort, request, render_template
from uuid6 import uuid7
from faker import Factory

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
db_name = "first.db"

# ready user and post data
fake = Factory.create('ja_JP')

# print('start to initialize')

# # name, id
# users = []
# for idx in range(0x80):
#     name = fake.romanized_name().replace(' ', '_')
#     # meet unique constraint
#     while not all(user[0] != name for user in users):
#         name = fake.romanized_name().replace(' ', '_')
#     users.append((name, str(uuid7())))
#     time.sleep(random.random())
# # user_name, body
# posts = []
# for idx in range(0xff):
#     posts.append((random.choice(users)[0], fake.sentence()))

# print('finish to initialize')

# # initialize db
# if os.path.exists(db_name):
#     os.remove(db_name)
# c = sqlite3.connect(db_name)
# c.execute("CREATE TABLE IF NOT EXISTS users (name STRING PRIMARY KEY, id STRING UNIQUE)")
# c.execute("PRAGMA foreign_keys = true")
# c.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name STRING, body STRING, foreign key (user_name) references users(name))")
# c.executemany("INSERT INTO users (name, id) VALUES (?, ?)", users)
# c.executemany("INSERT INTO posts (user_name, body) VALUES (?, ?)", posts)
# c.commit()
# c.close()

@app.route("/<path:path>")
def missing_handler(path):
    abort(404, "not found")

class Index_get_response:
    def __init__(self, response_from_db: tuple) -> None:
        if response_from_db is None or len(response_from_db) != 3:
            raise TypeError('response_from_db must be tuple whose size is 3.')
        id, user_name, body = response_from_db
        if type(id) != int or type(user_name) != str or type(body) != str:
            raise TypeError('response_from_db must be (int, str, str) tuple.')
        self.id = id
        self.user_name = user_name
        self.body = body

@app.route("/", methods=["GET"])
def index_get():
    q = ''
    if request.args.get('q') is not None:
        q = request.args.get('q')
    
    results = None
    c = sqlite3.connect(db_name)
    try:
        cur = c.cursor()
        cur.execute(f"SELECT posts.id, users.name, posts.body FROM posts INNER JOIN users ON posts.user_name = users.name AND posts.body LIKE \'%{q}%\'")
        results = cur.fetchall()
    except Exception as e:
        traceback.print_exc()
        return f'error: {e}', 500
    finally:
        c.close()

    results_resp = [Index_get_response(result) for result in results]
    return render_template('index.html', results=results_resp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31555)
