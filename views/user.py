from flask import render_template, Blueprint, g
from models import User
from flask_login import login_required
from forms import ChangeInfoForm, ChangePasswordForm


main = Blueprint('user', __name__)


@main.route('/<string:username>/info')
@login_required
def info(username):
    return render_template('user/info.html',
                           view_user=User.view(username))


@main.route('/setting')
@login_required
def setting():
    return render_template('user/setting.html',
                           info_form=ChangeInfoForm(),
                           password_form=ChangePasswordForm(),
                           user=g.user)


