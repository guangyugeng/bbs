from flask import render_template, redirect, url_for, request
from flask_login import logout_user, login_required
from flask import g, Blueprint
from forms import LoginForm, RegisterForm
from controller import post

from utils.utils import log

main = Blueprint('general', __name__)


@main.route('/', methods = ['GET'])
def index():
    page = request.args.get('page', '1')
    data = post.topic_page(page)
    return render_template('general/index.html',
                               **data)


@main.route('/go/<string:node_name>')
def node_index(node_name):
    log("hello")
    page = request.args.get('page', '1')
    log("hello")
    data = post.node_page(page,node_name)
    return render_template('general/node.html',
                               **data)


@main.route('/<string:topic_name>')
def topic_index(topic_name):
    page = request.args.get('page', '1')
    data = post.topic_page(page, topic_name)
    return render_template('general/index.html',
                               **data)


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


