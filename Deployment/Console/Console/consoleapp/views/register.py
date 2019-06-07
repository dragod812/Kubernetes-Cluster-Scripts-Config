from flask import Blueprint, render_template
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from consoleapp import app, db
from consoleapp.views.forms import RegistrationForm
from consoleapp.views.models import User, Company

reg = Blueprint('register', __name__)

@reg.route('/register', methods=['GET', 'POST'])
def register() :
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        
        my_company = Company.query.filter_by(company_name=form.company.data).first()
        
        if my_company is None:
            my_company = Company(company_name=form.company.data)
            db.session.add(my_company)
            db.session.commit()



        user = User(username=form.username.data, email=form.email.data, company_id=my_company.id)
       
        user.set_password(form.password.data)
        db.session.add(user)        
        db.session.commit()
        return redirect(url_for('login.login'))
    return render_template('register.html', title='Register', form=form)