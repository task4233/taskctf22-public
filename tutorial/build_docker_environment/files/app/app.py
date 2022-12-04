from flask import Flask, abort, render_template
import os

app = Flask(__name__)

@app.route("/<path:path>")
def missing_handler(path):
    abort(404, "not found")

@app.route("/", methods=["GET"])
def index_get():
    # enable the line below!
	# return render_template('index.html', flag=os.getenv('FLAG'))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=31777)

