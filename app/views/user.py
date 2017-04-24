from flask import render_template, flash, session, redirect, url_for,Blueprint,abort,request,g
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime


main = Blueprint('user', __name__)
#
#
# @main.before_request
# def before_request():
#     g.user = current_user
#     if g.user.is_authenticated:
#         g.user.last_seen = datetime.now()
#         g.user.save()
#

# @main.route('/user/<username>')
# @login_required
# def info(username):
#     user = User.query.filter_by(username = username).first()
#     if user == None:
#         flash('User ' + username + ' not found.')
#         return redirect(url_for('index'))
#
#     return render_template('user/user.html',
#         user = user,
#                            )

@main.route('/<string:username>/info')
# @login_required
def info(username):
    data = User.view(username)
    return render_template('user.info.html', **data)


@main.route('/<string:username>/setting')
@login_required
def setting(username):
    return render_template('user.setting.html')


#
# @main.route('/edit_user', methods=['GET', 'POST'])
# @login_required
# def edit_user():
#
#     return render_template('user/edit_user.html')
