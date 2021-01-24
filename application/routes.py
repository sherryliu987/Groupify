import os.path
from os import path, abort
from flask import send_from_directory, flash, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename

from application import app

ALLOWED_EXTENSIONS = {'csv', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
@app.route("/main",  methods=['GET', 'POST'])
def home():
    print("HELLO")
    if request.method == 'POST':
        if 'people' not in request.files:
            print("MADE IT HERE1")
            flash('No file part')
            return redirect(request.url)
        file = request.files['people']
        if file.filename == '':
            flash('No selected file')
            print("MADE IT HERE2")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(request.files['people'].filename)
            print("MADE IT HERE")
            return redirect(url_for('groups', filename=filename))
    return render_template("main.html")

@app.route("/groups/<filename>")
def groups(filename="/"):
    f = open(filename)
    groups=[
        {"id": "1", "people": {"Bob", "Joe"}},
        {"id": "2", "people": {"Bob", "Joe"}},
        {"id": "3", "people": {"Bob", "Joe"}}
    ]
    return render_template("groups.html", groups = groups)

@app.route("/about")
def about():
    return render_template("about.html")