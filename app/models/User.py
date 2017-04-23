# from app import db
# from .Base import ModelMin, timestamp
# from hashlib import md5
# import time
# from functools import wraps
# from utils import log
#
# ROLE_USER = 0
# ROLE_ADMIN = 1
#
#
#
#
# class User(db.Model, ModelMin):
#     __tablename__ = 'user'
#
#     id = db.Column(db.Integer, primary_key = True)
#     username = db.Column(db.String(64), unique = True)
#     nickname = db.Column(db.String(64), unique = True)
#     email = db.Column(db.String(120), index = True, unique = True)
#     password = db.Column(db.String(120), index = True)
#     # role = db.Column(db.SmallInteger, default = ROLE_USER)
#     # user_info= db.Column(db.String(140))
#     last_seen = db.Column(db.DateTime)
#
#     posts = db.relationship('Post', lazy='dynamic',cascade="delete, delete-orphan", backref='user')
#     comments = db.relationship('Comment', lazy='dynamic',cascade="delete, delete-orphan", backref='user')
#
#     def __init__(self, form):
#         # r = self.register_valid(form)
#         # if r['valid'] == False:
#         #     k,v = r['msg'].popitem()
#         #     raise ValueError('msg{}:{}'.format(k,v) )
#         self.username = form.get('username', '')
#         self.password = form.get('password', '')
#         self.nickname = form.get('nickname', '')
#         self.email = form.get('email', '')
#
#     @staticmethod
#     def view(username):
#         # data = {}
#         user = User.query.filter_by(username=username).first()
#         # data['view_user'] = user
#         return user.__dict__
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return str(self.id)
#
#     # def avatar(self, size):
#     #     return 'http://www.gravatar.com/avatar/' + md5(self.email.encode(encoding='UTF-8',errors='strict')).hexdigest()+ '?d=mm&s=' + str(size)
#
#     def __repr__(self):
#         return '<User %r>' % (self.username)
#
#
#     # @staticmethod
#     # def login_valid(function):
#     #     @wraps(function)
#     #     def wrapper(*args, **kwargs):
#     #         form = args[0]
#     #         username = form.get('username')
#     #         password = form.get('password')
#     #         u = User.query.filter_by(username=username).first()
#     #         valid = u is not None and u.password == password
#     #         r = dict(
#     #             valid=valid,
#     #             user=u,
#     #             msg=dict()
#     #         )
#     #         msg = r['msg']
#     #         if not valid:
#     #             msg['.login-message'] = '用户名或密码错误'
#     #         args = form, r
#     #         return function(*args, **kwargs)
#     #     return wrapper
#
#
#     @classmethod
#     def register_valid(cls, form):
#         username = form.get('username')
#         nickname = form.get('nickname')
#         password = form.get('password')
#         confirm_password = form.get('confirm')
#         email = form.get('email')
#         un_valid_msg = cls._username_valid(username)
#         nn_valid_msg = cls._nickname_valid(nickname)
#         pw_valid_msg = cls._password_valid(password, confirm_password)
#         e_valid_msg = cls._email_valid(email)
#         un_valid = un_valid_msg['valid']
#         nn_valid = nn_valid_msg['valid']
#         pw_valid = pw_valid_msg['valid']
#         e_valid = e_valid_msg['valid']
#         msg = dict()
#         msg.update(un_valid_msg['msg'])
#         msg.update(nn_valid_msg['msg'])
#         msg.update(pw_valid_msg['msg'])
#         msg.update(e_valid_msg['msg'])
#         # log(un_valid,pw_valid,e_valid)
#         r = dict(
#             valid=un_valid and pw_valid and e_valid and nn_valid,
#             msg=msg
#         )
#         return r
#
#     @staticmethod
#     def _username_valid(username):
#         result = dict(
#             valid=False,
#             msg=dict()
#         )
#         str_valid = True
#         # log(username)
#         username = username.strip()
#         # for c in username:
#         #     if c not in valid_str:
#         #         str_valid = False
#         length_valid = 8 <= len(username) <= 20
#         u = User.query.filter_by(username=username).first()
#         not_exist = u is None
#         result['valid'] = str_valid and length_valid and not_exist
#         # log(type(result['msg']))
#         msg = result['msg']
#         if not str_valid:
#             msg['.username-message']='输入8-20位用户名,只能使用英文字母、下划线及数字'
#         elif not length_valid:
#             msg['.username-message']='输入8-20位用户名,只能使用英文字母、下划线及数字'
#         elif not not_exist:
#             msg['.username-message']= '用户名已存在'
#         return result
#
#
#     @staticmethod
#     def _nickname_valid(nickname):
#         result = dict(
#             valid=False,
#             msg=dict()
#         )
#         str_valid = True
#         # log(nickname)
#         nickname = nickname.strip()
#         # for c in username:
#         #     if c not in valid_str:
#         #         str_valid = False
#         length_valid = 2 <= len(nickname) <= 20
#         u = User.query.filter_by(nickname=nickname).first()
#         not_exist = u is None
#         result['valid'] = str_valid and length_valid and not_exist
#         # log(type(result['msg']))
#         msg = result['msg']
#         if not str_valid:
#             msg['.username-message']='输入2-20昵称,只能使用英文字母、下划线及数字'
#         elif not length_valid:
#             msg['.username-message']='输入2-20昵称,只能使用英文字母、下划线及数字'
#         elif not not_exist:
#             msg['.username-message']= '昵称已存在'
#         return result
#
#
#     @staticmethod
#     def _password_valid(password, confirm_password):
#         result = dict(
#             valid=False,
#             msg=dict()
#         )
#         password = password.strip()
#         str_valid = True
#         # for c in password:
#         #     if c not in valid_str:
#         #         str_valid = False
#         confirm_password = confirm_password.strip()
#         length_valid = 8 <= len(password) <= 20
#         confirm_valid = password == confirm_password
#         result['valid'] = str_valid and length_valid and confirm_valid
#         msg = result['msg']
#         if not str_valid:
#             msg['.password-message'] = '输入8-20位密码,只能使用英文字母、下划线及数字'
#         if not length_valid:
#             msg['.password-message'] = '输入8-20位密码,只能使用英文字母、下划线及数字'
#         if not confirm_valid:
#             msg['.confirm-message'] = '重复输入的密码'
#         return result
#
#
#     @staticmethod
#     def _email_valid(email):
#         result = dict(
#             valid=False,
#             msg=dict()
#         )
#         str_valid = True
#         email = email.strip()
#         # for c in email:
#         #     if c not in email_valid_str:
#         #         str_valid =False
#
#         split_email = email.split('@', 1)
#         split_valid = len(split_email) == 2
#         not_exist = False
#         if split_valid and split_email[0] != '' and split_email[1] != '':
#             host = split_email[1]
#             split_host = host.split('.', 1)
#             split_valid = len(split_host) == 2
#             if split_valid and split_host[0] != '' and split_host[1] != '':
#                 u = User.query.filter_by(email=email).first()
#                 if u is None:
#                     not_exist = True
#         else:
#             str_valid = False
#         result['valid'] = str_valid and not_exist
#         msg = result['msg']
#         if not str_valid:
#             msg['.email-message'] = '请输入正确的邮箱'
#         elif not not_exist:
#             msg['.email-message'] = '邮箱已被注册'
#         return result
