from flask import Flask, session, redirect, url_for, escape, request, Blueprint, render_template
from flask_login import login_required, current_user
from .models import Project, ProjectPermission, ProjectUserPermission, Job, DataLoadJob, SFTPJob
from consoleapp import db
from consoleapp.views.forms import SFTPForm
from consoleapp.k8s import api_instance, getJobBody, ENV_LIST
from kubernetes.client.rest import ApiException

sftpbp = Blueprint('sftp', __name__)

@sftpbp.route('/project/<projectid>/sftp', methods=['GET', 'POST'])
@login_required
def sftp(projectid):
    acess_permision = ProjectPermission.query.filter_by(project_permission_name = 'access').first()
    acess_permision_id = acess_permision.id
    this_projectpermission = ProjectUserPermission.query.filter_by(project_id = projectid, u_id = current_user.id, project_permission_id= acess_permision_id).first()
    project = Project.query.filter_by(id = projectid).first()
    if this_projectpermission is None :
        return redirect(url_for('index.index'))
    else :
        form = SFTPForm()
        if form.validate_on_submit():
            print("projectid:",projectid)
            sftpjob = SFTPJob(job_type='SFTPJob', project_id=projectid, hostname=form.hostname.data, username=form.username.data,password=form.password.data,file_path=form.file_path.data)
            db.session.add(sftpjob)
            db.session.commit()
            ENV_LIST['SFTP_HOSTNAME']= sftpjob.hostname
            ENV_LIST['JOB_ID']= str(sftpjob.id)
            ENV_LIST['SFTP_USERNAME']= sftpjob.username
            ENV_LIST['SFTP_PASSWORD']= sftpjob.password
            ENV_LIST['SFTP_REMOTE_PATH']= sftpjob.file_path
            ENV_LIST['HADOOP_DIRECTORY']= "/" + str(projectid) + "/" + str(sftpjob.id)#decide how to store files
            jobname = 'job'+str(sftpjob.id)
            job_body = getJobBody(namespace='couture-console', jobname=jobname, containername=jobname, containerimage='sidharthc/nifi-test:alpha', env_vars=ENV_LIST, containerargs=['SFTP_TO_HDFS.py'])
            try:
                api_response = api_instance.create_namespaced_job("couture-console", job_body, pretty=True)
                print(api_response)
            except ApiException as e:
                print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)
    return render_template('sftp.html', form = form, project =project)
