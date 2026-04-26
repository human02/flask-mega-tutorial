from app import flask_app
from flask import render_template


@flask_app.route("/")
@flask_app.route("/index")
def index():
    user = {"username": "John Doe"}
    return render_template("index.html", title="Home", user=user)
