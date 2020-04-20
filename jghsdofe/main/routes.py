from flask import render_template, url_for, redirect, flash, request, Blueprint, current_app, send_from_directory
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html.j2')


@main.route('/file/<path:filename>')
def file(filename):
    return send_from_directory('files', filename)
