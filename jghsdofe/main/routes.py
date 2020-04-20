from flask import render_template, url_for, redirect, flash, request, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html.j2')
