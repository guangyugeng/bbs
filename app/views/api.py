from flask import request, g, Blueprint, jsonify, redirect, abort, flash, url_for
import json
from utils import log
from app import db
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app.controller import user

main = Blueprint('api', __name__)


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    log(form)
    r = user.login(form)
    log(r)
    if r['valid']:
        log("success")
        return redirect(url_for('general.index'))
    else:
        log("fails")
        flash(list(r['msg'].values()).__str__())
        # flash(r['msg'].popitem()[1])
        return redirect(url_for('general.login_register'))
 # dict

@main.route('/register', methods=['POST'])
def register():
    log('r')
    form = request.form
    log('rr')
    r = user.register(form)
    if r['valid']:
        flash('注册成功')
        log("success")
    else:
        log("fails")
        flash(list(r['msg'].values()).__str__())
    return redirect(url_for('general.login_register'))

@main.route('/change_info', methods=['POST'])
def change_info():
    log('r')
    form = request.form
    log('rr')
    r = user.change_info(form)
    if r['valid']:
        flash('修改成功')
        log("success")
    else:
        log("fails")
        flash(list(r['msg'].values()).__str__())
    return redirect(url_for('user.setting'))
list
@main.route('/change_password', methods=['POST'])
def change_password():
    log('r')
    form = request.form
    log('rr')
    r = user.change_password(form)
    if r['valid']:
        flash('修改成功')
        log("success")
    else:
        log("fails")
        flash(list(r['msg'].values()).__str__())
    return redirect(url_for('user.setting'))

# @main.route('/api/user/edit', methods=['POST'])
# @login_required
# def user_edit():
#     form = request.form
#     u = g.user
#     r = {
#         'data': []
#     }
#
#     if not u.valid():
#         r['success'] = True
#         r['username'] = u.username
#         g.user.nickname = User.make_unique_nickname(form['nickname'])
#         g.user.user_info = form['info']
#         g.user.save()
#         db.session.commit()
#     else:
#         r['success'] = False
#         message = u.error_message('edit')
#         r['message'] = message
#
#     return json.dumps(r, ensure_ascii=False)
#
