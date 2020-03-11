from . import server
from flask import render_template


@server.route("/")
def dashboard():
    return render_template("dashboard.html")

