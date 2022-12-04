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

# ready user and post data
fake = Factory.create('ja_JP')
db_name = "first.db"

@app.route("/<path:path>")
def missing_handler(path):
    abort(404, "not found")

# NOTE: This handler is not unavailable
# @app.route("/register", methods=["POST"])
# def register_post():
#     data = request.json
#     c = sqlite3.connect(db_name)
#     c.execute(f"INSERT INTO users (name, id) VALUES ({data['name']}, {str(uuid7())})")
#     c.commit()
#     c.close()

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
