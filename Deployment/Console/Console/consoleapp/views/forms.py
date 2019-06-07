from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from consoleapp.views.models import User


def password_length_check(form, field):
    if len(field.data) < 8:
        raise ValidationError("Password must be atleast 8 characters")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    company = StringField("Company Name", validators=[DataRequired()])
    password = PasswordField(
        "Password", validators=[DataRequired(), password_length_check]
    )
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    """def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    """

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class UserControlForm(FlaskForm):
    u_id = IntegerField("Id")
    username = StringField("Username")
    email = StringField("Email")
    company = StringField("Company Name")
    active = BooleanField("Active")
    


class AllUsersForm(FlaskForm):
    allusers = FieldList(FormField(UserControlForm))
    submit = SubmitField("Save")


class UserForm(FlaskForm):
    u_id = IntegerField("Id")
    username = StringField("Username")
    email = StringField("Email")
    proj_access = BooleanField("Access")



class NewProjectForm(FlaskForm):
    project_name =  StringField("Project Name", validators=[DataRequired()])
    project_description = StringField("Project Description", validators=[DataRequired()])

    company_users = FieldList(FormField(UserForm))

    submit = SubmitField("Create New Project")

class SFTPForm(FlaskForm):
    hostname =  StringField("Hostname/IP Address", validators=[DataRequired()])
    username =  StringField("Username", validators=[DataRequired()])
    password =  StringField("Password", validators=[DataRequired()])
    file_path =  StringField("File Path", validators=[DataRequired()])

    submit = SubmitField("Submit")


