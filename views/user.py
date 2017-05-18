from flask import render_template, Blueprint, g
from models import User
from flask_login import login_required
from f.forms import ChangeInfoForm, ChangePasswordForm

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
@login_required
def info(username):
    # view_user =
    # check_user = g.user
    return render_template('user/info.html',
                           view_user=User.view(username))


@main.route('/setting')
@login_required
def setting():
    # user = g.user
    # info_form = ChangeInfoForm()
    # password_form = ChangePasswordForm()
    return render_template('user/setting.html',
                           info_form=ChangeInfoForm(),
                           password_form=ChangePasswordForm(),
                           user=g.user)


#
# @main.route('/edit_user', methods=['GET', 'POST'])
# @login_required
# def edit_user():
#
#     return render_template('user/edit_user.html')