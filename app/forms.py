from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import DataRequired, Email, Length


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

# from flask_wtf import Form
# from wtforms.fields import *
# from wtforms.validators import Required, Email
#
#
# class SignupForm(Form):
#     name = StringField(u'Your name', validators=[Required()])
#     password = PasswordField(u'Your favorite password', validators=[Required()])
#     email = StringField(u'Your email address', validators=[Email()])
#     birthday = DateField(u'Your birthday')
#
#     a_float = FloatField(u'A floating point number')
#     a_decimal = DecimalField(u'Another floating point number')
#     a_integer = IntegerField(u'An integer')
#
#     now = DateTimeField(u'Current time',
#                         description='...for no particular reason')
#     sample_file = FileField(u'Your favorite file')
#     eula = BooleanField(u'I did not read the terms and conditions',
#                         validators=[Required('You must agree to not agree!')])
#
#     submit = SubmitField(u'Signup')

