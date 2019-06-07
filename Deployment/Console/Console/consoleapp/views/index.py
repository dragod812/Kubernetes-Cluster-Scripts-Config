from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template
from flask_login import login_required, current_user
from consoleapp.views.models import Project, ProjectUserPermission, ProjectPermission
from consoleapp import db

home = Blueprint('index', __name__)

@home.route('/')
@home.route('/index')
@login_required
def index():
    acess_permision = ProjectPermission.query.filter_by(project_permission_name = 'access').first()
    acess_permision_id = acess_permision.id
    projectpermission = ProjectUserPermission.query.filter_by(u_id = current_user.id, project_permission_id= acess_permision_id).all()
    projects = []
    for myprojectpermission in projectpermission:
        myprojectid = myprojectpermission.project_id
        myproject = Project.query.filter_by(id = myprojectid).first()
        projects.append(myproject)

    
    return render_template('index.html', projects = projects)