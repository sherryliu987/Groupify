import os.path
from os import path, abort
from flask import send_from_directory, flash, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
from itertools import permutations

from application import app

ALLOWED_EXTENSIONS = {'xls'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
@app.route("/main", methods=['GET', 'POST'])
def home(message=""):
    if request.method == 'POST':
        print(request.form)
        num_groups = request.form.get('num_groups')
        if 'people' not in request.files:
            return render_template("main.html", message="Please choose a valid file.")
        file = request.files['people']
        if file.filename == '':
            return render_template("main.html", message="Please choose a valid file.")
        if num_groups == '':
            return render_template("main.html", message="Please input your desired number of groups.")
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(request.files['people'].filename)
            return redirect(url_for('groups', filename=filename, num_groups=num_groups))
    return render_template("main.html", message=message)


@app.route("/groups/<filename>/<num_groups>")
def groups(filename="/", num_groups=1):
    f=send_from_directory("../", filename)

    df = pd.read_excel(filename)
    print(df)
    print(num_groups)
    final_groups = [
        {"id": "1", "people": {"Bob", "Joe"}},
        {"id": "2", "people": {"Bob", "Joe"}},
        {"id": "3", "people": {"Bob", "Joe"}}
    ]
    return render_template("groups.html", groups=final_groups)


@app.route("/about")
def about():
    return render_template("about.html")
