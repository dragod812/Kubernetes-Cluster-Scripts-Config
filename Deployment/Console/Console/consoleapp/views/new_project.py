from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template
from flask_login import login_required, current_user
from .models import Project, Company, User, ProjectUserPermission, ProjectPermission
from consoleapp import db
from consoleapp.views.forms import NewProjectForm, UserForm
new_proj = Blueprint('new_project', __name__)

@new_proj.route('/new_project', methods=['GET', 'POST'])
@login_required
def new_project():
    my_company_id = current_user.company_id
    #print("my_company_id:",my_company_id)
    my_company = Company.query.filter_by(id = my_company_id).first()
    users = my_company.employees
    form = NewProjectForm()
    for user in users:  
        if user.id != current_user.id :
            userform = UserForm()
            userform.u_id = user.id           
            userform.username = user.username
            userform.email = user.email
            userform.proj_access = False
            form.company_users.append_entry(userform)

    
    if form.validate_on_submit():  
        my_company_id = current_user.company_id        
        my_project = Project(project_name = form.project_name.data, project_description= form.project_description.data, company_id = my_company_id)
        db.session.add(my_project)
        db.session.commit()

        acess_permision = ProjectPermission.query.filter_by(project_permission_name = 'access').first()
        acess_permision_id = acess_permision.id
        my_user_project_permission = ProjectUserPermission(project_id= my_project.id, u_id= current_user.id, project_permission_id= acess_permision_id)
        db.session.add(my_user_project_permission)
        db.session.commit()

        selected_users = request.form.getlist("accessList") 
        for u_id in selected_users :
            my_user_project_permission = ProjectUserPermission(project_id= my_project.id, u_id= u_id, project_permission_id= acess_permision_id)
            db.session.add(my_user_project_permission)
        
        db.session.commit()
        return redirect(url_for('index.index'))
    return render_template('new_project.html', form = form)