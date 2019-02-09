import os
from flask import Flask, render_template, request, Markup, flash
from analyzeImage import run

app = Flask(__name__)
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
	res = run(f)
	print(res+"\n")
	res = Markup("<p>"+res+"</p>")
	flash(res)
	return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
