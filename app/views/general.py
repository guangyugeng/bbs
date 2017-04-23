from flask import render_template, flash, session, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask import g, Blueprint
from datetime import datetime
from app import db, lm
from app.models.User import User, ROLE_USER, ROLE_ADMIN
from app.forms import LoginForm, RegisterForm
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
# import wtforms.q
from markupsafe import escape


main = Blueprint('general', __name__)

# @main.route('/')
# def login_view():
#     u = g.user
#     if u is not None:
#         return redirect(url_for('general.index'))
#     return render_template('login.html')

@main.route('/')
@main.route('/index', methods = ['GET', 'POST'])
def index():
    print(g.user,'sdsds')
    user = g.user
    if user.is_authenticated:
        return render_template('general/index.html',
                               user = user)
    else:

        return render_template('general/index.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route('/login_register', methods = ['GET', 'POST'])
def login_register():
    # login_form = LoginForm()
    # register_form = RegisterForm()
    u = g.user
    if u.is_authenticated:
        return redirect(url_for('general.index'))
    else:
        return render_template('general/login_register.html')
                              # title = 'Sign In',
                              # login_form = login_form,
                              # register_form = register_form)


@login_required
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('general.login_view'))


@main.errorhandler(404)
def internal_error(error):
    return render_template('base/404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base/500.html'), 500
