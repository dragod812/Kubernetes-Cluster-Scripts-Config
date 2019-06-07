from flask import Blueprint, render_template, redirect, url_for
from flask_login import logout_user


mod1 = Blueprint('logout', __name__)

@mod1.route('/logout')
def logout() :
    logout_user()
    return redirect(url_for('login.login'))
