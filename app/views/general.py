from flask import render_template, flash, session, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from flask import g, Blueprint
from datetime import datetime
from app import db, lm
from app.models import User, ROLE_USER, ROLE_ADMIN
from app.forms import LoginForm, RegisterForm
from app.controller import post
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

@main.route('/', methods = ['GET'])
def index():
    # print(g.user,'sdsds')
    page = request.args.get('page', '1')
    data = post.page(page)
    u = g.user
    if u.is_authenticated:
        return render_template('general/index.html',
                               user = u,
                               **data)
    else:
        return render_template('general/index.html',
                               **data)

@main.route('/<string:node_name>')
def node_index(node_name):
    page = request.args.get('page', '1')
    data = post.page(page,node_name)
    print(data['selected_node'])
    for n in data['node_list']:
        print(n.name==data['selected_node'])
    u = g.user
    if u.is_authenticated:
        return render_template('general/index.html',
                               user = u,
                               **data)
    else:
        return render_template('general/index.html',
                               **data)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@main.route('/login_register', methods = ['GET'])
def login_register():
    login_form = LoginForm()
    register_form = RegisterForm()
    u = g.user
    if u.is_authenticated:
        return redirect(url_for('general.index'))
    else:
        return render_template('general/login_register.html',
                              login_form = login_form,
                              register_form = register_form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('general.index'))


@main.errorhandler(404)
def internal_error(error):
    return render_template('base/404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base/500.html'), 500
