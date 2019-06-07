from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template
from flask_login import login_required
from .models import User
from consoleapp import db
from .forms import AllUsersForm, UserForm

adminmod1 = Blueprint('user_control_panel', __name__)


@adminmod1.route('/user_control_panel', methods=['GET', 'POST'])
@login_required
def user_control_panel():
    users = User.query.filter_by(active = True).all()
    form = AllUsersForm()
    for user in users:  
        userform = UserControlForm()
        userform.u_id = user.id           
        userform.username = user.username
        userform.email = user.email
        userform.company = user.company_id
        userform.active = user.active

        form.allusers.append_entry(userform)

    if form.is_submitted(): 
        #Code to update User table   
        selected_users = request.form.getlist("verifyList") 
        #print("Verify")
        for u_id in selected_users :
            my_user = User.query.filter_by(id= u_id).first()
            my_user.active= True
            db.session.commit()
        db.session.commit()
        return redirect(url_for('index.index'))
    return render_template('user_control_panel.html', form = form)