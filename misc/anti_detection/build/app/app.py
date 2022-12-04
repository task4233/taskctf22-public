from flask import Flask, abort, render_template, request
import os
from subprocess import STDOUT, check_output
import ssdeep
import stat
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'

@app.route("/<path:path>")
def missing_handler(path):
    abort(404, "not found")

@app.route("/", methods=["GET"])
def index_get():
	return render_template('index.html', flag='None')

@app.route("/", methods=["POST"])
def index_post():
    blacklist_file_hash = '96:RVYhTLoB+Bk6XDW1RZxpUZuPc/KL/jDmjmwtEKUbGw7smuB3yfBqviOIm0s:RCIwesgRZxpU2cyLHKT4bPEEsvivm'
    file = request.files['file'].read()

    # calc hash value
    hash_val = ssdeep.hash(file)
    if int(ssdeep.compare(hash_val, blacklist_file_hash)) >= 80:
        return render_template('index.html', flag='this file is similar to the file in blacklisted')

    # save given file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], str(uuid.uuid4()))
    with open(file_path, 'wb') as f:
        f.write(file)
    os.chmod(file_path, os.stat(file_path).st_mode | stat.S_IEXEC)
    
    # execute value
    output = check_output(file_path, stderr=STDOUT, timeout=1)

    # check cheating
    if output.decode() != f'flag: {os.getenv("FLAG")}':
        return render_template('index.html', flag='invalid output')
    return render_template('index.html', flag=output.decode())

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=31516)

