from flask import Flask

UPLOAD_FOLDER = "/uploads"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret_key"

from application import routes