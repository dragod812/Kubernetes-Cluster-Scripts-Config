from datetime import datetime
from consoleapp import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class Company(db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key=True)
    
    company_name  = db.Column(db.String(64), index=True)
    status = db.Column(db.String(64), index=True, default='default')

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    employees = db.relationship("User", backref=db.backref("Company", lazy="joined"))
    projects = db.relationship("Project", backref=db.backref("Company", lazy="joined"))

    def __init__(self, id=None, company_name=None):
        self.id = id
        self.company_name = company_name
           
    def __repr__(self):
        mylist = [self.id, self.company_name]
        return '<Company id:{}, name: {} >'.format(*mylist)

    def is_active(self):
        return self.active
    

    

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=False)
 

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id=None, username=None, email=None, company_id=None):
        self.id = id
        self.username = username
        self.email = email
        self.company_id = company_id
        
    
    def __repr__(self):
        mylist = [self.id, self.username]
        return '<User id:{}, username: {} >'.format(*mylist)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return self.active

    def u_id(self):
        return self.id

class Project(db.Model):
    __tablename__ = 'Project'
    id = db.Column(db.Integer, primary_key=True)

    project_name = db.Column(db.String(64), index=True)
    project_description = db.Column(db.Text)

    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=False)
    
    jobs = db.relationship("Job", backref=db.backref("Project", lazy="joined"))

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id=None, project_name=None, project_description = None, company_id=None):
        self.id = id
        self.project_name = project_name
        self.project_description = project_description
        self.company_id = company_id

    def is_active(self):
        return self.active

    def project_id(self):
        return self.id
    
 



class ProjectPermission(db.Model):
    __tablename__ = 'ProjectPermission'
    id = db.Column(db.Integer, primary_key=True)

    project_permission_name = db.Column(db.String(64), index=True, nullable=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id=None, project_permission_name=None):
        self.id = id
        self.project_permission_name = project_permission_name



class ProjectUserPermission(db.Model):
    __tablename__ = 'ProjectUserPermission'
    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer,db.ForeignKey('Project.id'), nullable=False)
    project = db.relationship("Project")

    u_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    user = db.relationship("User")

    project_permission_id = db.Column(db.Integer, db.ForeignKey('ProjectPermission.id'), nullable=False)
    project_permission = db.relationship("ProjectPermission")

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id=None, project_id=None, u_id=None, project_permission_id=None):
        self.id = id
        self.project_id = project_id
        self.u_id = u_id
        self.project_permission_id = project_permission_id
        
    
       
class Job(db.Model):
    __tablename__ = 'Job'
    id = db.Column(db.Integer, primary_key=True)

    job_status = db.Column(db.String(64), index=True, default = 'default')
    job_type = db.Column(db.String(64), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey('Project.id'), nullable=False)

    active = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_on':job_type,
    }

    def __init__(self, id=None, job_type=None, project_id=None):
        self.id = id
        self.job_type = job_type
        self.project_id = project_id

    def is_active(self):
        return self.active


class DataLoadJob(Job):
    __tablename__ = 'DataLoadJob'

    id = db.Column(db.Integer, db.ForeignKey('Job.id'), primary_key=True)
   
    files = db.relationship("DataLoadFile", backref=db.backref("DataLoadJob", lazy="joined"))
    __mapper_args__ = {
        'polymorphic_identity':'DataLoad'
    }

    def __init__(self, id=None, job_type=None, project_id=None):
        super(DataLoadJob, self).__init__(id, job_type=job_type, project_id=project_id)

        
class DataLoadFile(db.Model):
    __tablename__ = 'DataLoadFile'

    job_id = db.Column(db.Integer, db.ForeignKey('DataLoadJob.id'), primary_key=True)
    filename =  db.Column(db.String(64), primary_key=True, nullable=False)
    transferred = db.Column(db.Boolean, default = 0)

    def __init__(self, job_id = None, filename = None):
        self.job_id = job_id
        self.filename = filename






class SFTPJob(DataLoadJob):
    __tablename__ = 'SFTPJob'

    id = db.Column(db.Integer, db.ForeignKey('DataLoadJob.id'), primary_key=True)

    hostname =  db.Column(db.String(64))
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    file_path = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity':'SFTPJob'
    }

    def __init__(self, id=None, job_type=None, project_id=None, hostname=None, username=None, password=None, file_path=None):
        super(SFTPJob, self).__init__(id, job_type=job_type, project_id=project_id)
        self.hostname = hostname
        self.username = username
        self.password = password
        self.file_path = file_path



@login.user_loader
def load_user(id):
    return User.query.get(int(id))
