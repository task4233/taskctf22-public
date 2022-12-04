import sys
import io
from flask import Flask, abort, request, render_template

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)

@app.route("/<path:path>")
def missing_handler(path):
    abort(404, "not found")

@app.route("/robots.txt", methods=["GET"])
def robots_get():
    return render_template('robots.txt')

@app.route("/admin/flag", methods=["GET"])
def flag_get():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    
    if ip == '127.0.0.1':
        return render_template("flag.html")
    else:
        return render_template("401.html", ip=ip)

@app.route("/", methods=["GET"])
def index_get():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=31481)
