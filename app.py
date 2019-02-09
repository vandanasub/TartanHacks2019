import os
from flask import Flask, render_template, request, Markup, flash
from flask_bootstrap import Bootstrap
from pdf import parse
import subprocess

app = Flask(__name__)
#Bootstrap(app)
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
	(res, keyPhr) = parse(f)
	res = Markup("<p>"+res+"</p>")
	print(res)
	# res1 = subprocess.run(["python","test.py", "foo bar"])
	# print(res1.stdout)
	flash(res,'message')
	for word in keyPhr:
		flash(word, 'keyPhrase')
	#print(message.sid)
	return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
