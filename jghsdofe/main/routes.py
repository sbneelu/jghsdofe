from flask import render_template, url_for, redirect, flash, request, Blueprint, current_app, send_from_directory
import os
from werkzeug import secure_filename

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html.j2')


@main.route('/file/<string:level>/<path:filename>')
def file(level, filename):
    return send_from_directory('files/' + secure_filename(level), secure_filename(filename))
