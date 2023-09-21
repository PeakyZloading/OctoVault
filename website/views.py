from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/overview', methods=['GET', 'POST'])
def overview():
    return render_template("overview.html")