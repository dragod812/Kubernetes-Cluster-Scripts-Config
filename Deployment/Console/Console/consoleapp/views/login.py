from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from consoleapp import app, db
from consoleapp.views.forms import LoginForm
from consoleapp.views.models import User, Company
mod = Blueprint('login', __name__)

@mod.route('/login', methods=['GET', 'POST'])
def login() :
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    
    if form.validate_on_submit():
        
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

