import os
from flask import Flask, render_template, request, Markup, flash
from flask_bootstrap import Bootstrap
from analyzeImage import run
import subprocess

app = Flask(__name__)
Bootstrap(app)
app.secret_key = os.urandom(24)
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/upload', methods=['POST'])
def upload_file():
	file = request.files['image']
	f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
	file.save(f)
	(res, keyPhr) = run(f)
	res = Markup("<p>"+res+"</p>")
	res1 = subprocess.run(["python","test.py", "foo bar"])
	print(res1.stdout)
	flash(res,'message')
	for word in keyPhr:
		flash(word, 'keyPhrase')
	return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
