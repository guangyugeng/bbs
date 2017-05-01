from flask import request, g, Blueprint, jsonify
from utils import log
import json

from app import db
from app.models import User
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app.controller import user

main = Blueprint('api', __name__)


@main.route('/login', methods=['POST'])
def login():
    form = request.get_json()
    r = user.login(form)
    log('r',r['msg'],r['valid'])
    return jsonify(r)


@main.route('/register', methods=['POST'])
def register():

    form = request.get_json()

    log('username',form['username'],type(form))
    # form1 = {
    #     'nickname' : form['nickname'],
    #     'email' : form['email'],
    #     'username' : form['username'],
    #     'password' : form['password']
    # }
    # log(form==form1)
    # assert register(form1)['valid'] == True

    r = user.register(form)
    log(('r',r['msg']))
    return jsonify(r)


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
