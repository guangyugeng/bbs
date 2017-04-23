# from flask import request, g, Blueprint
#
# import json
#
# from app import db
# from app.models import User
# from flask_login import login_user, logout_user, current_user, login_required
# from datetime import datetime
# from app.controller.user import login, register
#
# main = Blueprint('api', __name__)
#
#
# @main.before_request
# def before_request():
#     g.user = current_user
#     if g.user.is_authenticated:
#         g.user.last_seen = datetime.utcnow()
#         g.user.save()
#
#
# @main.route('/api/user/login', methods=['POST'])
# def user_login():
#     form = request.form
#     r = login(form)
#     return json.dumps(r, ensure_ascii=False)
#
#
# @main.route('/api/user/register', methods=['POST'])
# def user_register():
#     form = request.form
#     r = register(form)
#     return json.dumps(r, ensure_ascii=False)


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
