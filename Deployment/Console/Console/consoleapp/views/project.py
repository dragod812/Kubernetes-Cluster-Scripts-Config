from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template
from flask_login import login_required, current_user
from consoleapp.views.models import Project, Company, User, ProjectUserPermission, ProjectPermission, Job, DataLoadFile
from consoleapp import db
from consoleapp.views.forms import NewProjectForm, UserForm
from sqlalchemy import desc

proj = Blueprint('project', __name__)

@proj.route('/project/<projectid>')
@login_required
def project(projectid):
    acess_permision = ProjectPermission.query.filter_by(project_permission_name = 'access').first()
    acess_permision_id = acess_permision.id
    this_projectpermission = ProjectUserPermission.query.filter_by(project_id = projectid, u_id = current_user.id, project_permission_id= acess_permision_id).first()
    if this_projectpermission is None :
        return redirect(url_for('index.index'))
    else : 
        project = Project.query.filter_by(id = projectid).first()
        jobs = Job.query.filter_by(project_id = projectid).order_by(desc(Job.created)).all()  
    return render_template('project.html', project = project, jobs = jobs)