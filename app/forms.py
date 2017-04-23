from flask_wtf import Form
from wtforms.fields import *
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('SignIn')

class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    submit = SubmitField('SignUp')

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

