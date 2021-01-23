from flask import render_template

from application import app


@app.route("/")
@app.route("/main")
def home():
    return render_template("main.html")

@app.route("/groups")
def groups():
    return render_template("groups.html")