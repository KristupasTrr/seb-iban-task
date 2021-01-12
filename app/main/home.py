from flask import Blueprint, render_template

home_page = Blueprint('home', __name__, template_folder="templates")

"""
Endpoint for home page render
"""
@home_page.route("/", methods=["GET"])
def index():
    return render_template("index.html")