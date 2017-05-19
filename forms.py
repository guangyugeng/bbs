from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import DataRequired, Email, Length
from models import Node


class LoginForm(Form):
    login_username = StringField('login_username', validators=[DataRequired(),Length(min=3,max=20)])
    login_password = PasswordField('login_password', validators=[DataRequired(),Length(min=3,max=20)])
    submit = SubmitField('SignIn')


class RegisterForm(Form):
    register_username = StringField('register_username', validators=[DataRequired(),Length(min=3,max=20)])
    register_nickname = StringField('register_nickname', validators=[DataRequired(),Length(min=2,max=20)])
    register_password = PasswordField('register_password', validators=[DataRequired(),Length(min=6,max=20)])
    r_register_password = PasswordField('r_register_password', validators=[DataRequired(),Length(min=6,max=20)])
    register_email = StringField('register_email', validators=[Email(),Length(min=6,max=30)])
    r_register_email = StringField('r_register_email', validators=[Email(),Length(min=6,max=30)])
    submit = SubmitField('SignUp')


class ChangeInfoForm(Form):
    change_nickname = StringField('change_nickname', validators=[DataRequired(),Length(min=2,max=20)])
    change_email = StringField('change_email', validators=[Email(),Length(min=6,max=30)])
    r_change_email = StringField('r_change_email', validators=[Email(),Length(min=6,max=30)])


class ChangePasswordForm(Form):
    old_password = PasswordField('old_password', validators=[DataRequired(),Length(min=6,max=20)])
    change_password = PasswordField('change_password', validators=[DataRequired(),Length(min=6,max=20)])
    r_change_password = PasswordField('r_change_password', validators=[DataRequired(),Length(min=6,max=20)])


class AddPostForm(Form):
    title = StringField('title', validators=[DataRequired(),Length(min=2,max=20)])
    content = TextAreaField('content', validators=[DataRequired(),Length(min=20,max=1000)])
    node = SelectField('node', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__( *args,**kwargs)
        self.node.choices = [(node.id, node.name) for node in Node.query.order_by().all()]

