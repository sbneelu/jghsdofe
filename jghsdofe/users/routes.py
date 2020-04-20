from flask import render_template, url_for, redirect, flash, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from jghsdofe.users.forms import LoginForm, SignupForm, ChangePasswordForm
from jghsdofe.models import User
from jghsdofe import db, bcrypt
import requests
from jghsdofe.config import Config

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('users/login.html.j2', form=form, title='Login')


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    captcha_error = None
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignupForm()
    if form.validate_on_submit():
        if not request.form.get('g-recaptcha-response'):
            captcha_error = 'Please fill out the Captcha.'
            return render_template('users/signup.html.j2', form=form, title='Sign Up', captcha_error=captcha_error, captcha_sitekey=Config.RECAPTCHA_SITEKEY)
        payload = {
            'secret': Config.RECAPTCHA_SECRET,
            'response': request.form.get('g-recaptcha-response')
        }

        success = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload).json()['success']
        if not success:
            captcha_error = 'Invalid Captcha. Please try again.'
            return render_template('users/signup.html.j2', form=form, title='Sign Up', captcha_error=captcha_error, captcha_sitekey=Config.RECAPTCHA_SITEKEY)

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('users/signup.html.j2', form=form, title='Sign Up', captcha_error=captcha_error, captcha_sitekey=Config.RECAPTCHA_SITEKEY)


@users.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        flash('Your password has successfully been changed.', 'success')
        return redirect(url_for('main.index'))
    form.validate_on_submit()
    return render_template('users/change-password.html.j2', form=form, title='Change your Password')
