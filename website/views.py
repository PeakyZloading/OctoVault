from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/overview', methods=['GET'])
def overview():
    data = request.args
    fighter_name = request.args.get('octo_input')
    print(fighter_name)

    return render_template("overview.html")