from app.models import User
from flask_login import login_user
from functools import wraps
from utils import log


def login_valid(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        form = args[0]
        username = form.get('username')
        password = form.get('password')
        log(username)
        u = User.query.filter_by(username=username).first()
        log('valid',u)
        valid = u is not None and u.password == password
        r = dict(
            valid=valid,
            msg=dict()
        )
        msg = r['msg']
        if not valid:
            msg['.login-message'] = '用户名或密码错误'
        args = form, r
        return function(*args, **kwargs)
    return wrapper


def register_valid(function):
    def wrapper(*args, **kwargs):
        form = args[0]

        username = form.get('username')
        nickname = form.get('nickname')
        password = form.get('password')
        confirm_password = form.get('confirm')
        email = form.get('email')
        un_valid_msg = username_valid(username)
        nn_valid_msg = nickname_valid(nickname)
        pw_valid_msg = password_valid(password)
        e_valid_msg = email_valid(email)
        un_valid = un_valid_msg['valid']
        nn_valid = nn_valid_msg['valid']
        pw_valid = pw_valid_msg['valid']
        e_valid = e_valid_msg['valid']
        msg = dict()
        msg.update(un_valid_msg['msg'])
        msg.update(nn_valid_msg['msg'])
        msg.update(pw_valid_msg['msg'])
        msg.update(e_valid_msg['msg'])
        # log(un_valid,pw_valid,e_valid)
        r = dict(
            valid=un_valid and pw_valid and e_valid and nn_valid,
            msg=msg
        )
        args = form, r
        return function(*args, **kwargs)
    return wrapper


@login_valid
def login(form, r=dict):
    if r['valid']:
        db_u = User.query.filter_by(username=form['username']).first()
        log('login success')
        login_user(db_u)
    return r


@register_valid
def register(form, r=dict):
    log('register',r['valid'],r['msg'])
    if r['valid']:
        u = User(form)
        log('register')
        u.save()
    return r


def username_valid(username):
    result = dict(
        valid=False,
        msg=dict()
    )
    str_valid = True
    # log(username)
    username = username.strip()
    # for c in username:
    #     if c not in valid_str:
    #         str_valid = False
    length_valid = 8 <= len(username) <= 20
    u = User.query.filter_by(username=username).first()
    not_exist = u is None
    result['valid'] = str_valid and length_valid and not_exist
    # log(type(result['msg']))
    msg = result['msg']
    if not str_valid:
        msg['.username-message']='输入8-20位用户名,只能使用英文字母、下划线及数字'
    elif not length_valid:
        msg['.username-message']='输入8-20位用户名,只能使用英文字母、下划线及数字'
    elif not not_exist:
        msg['.username-message']= '用户名已存在'
    return result


def nickname_valid(nickname):
    result = dict(
        valid=False,
        msg=dict()
    )
    str_valid = True
    # log(nickname)
    nickname = nickname.strip()
    # for c in username:
    #     if c not in valid_str:
    #         str_valid = False
    length_valid = 2 <= len(nickname) <= 20
    u = User.query.filter_by(nickname=nickname).first()
    not_exist = u is None
    result['valid'] = str_valid and length_valid and not_exist
    # log(type(result['msg']))
    msg = result['msg']
    if not str_valid:
        msg['.username-message']='输入2-20昵称,只能使用英文字母、下划线及数字'
    elif not length_valid:
        msg['.username-message']='输入2-20昵称,只能使用英文字母、下划线及数字'
    elif not not_exist:
        msg['.username-message']= '昵称已存在'
    return result


def password_valid(password):
    result = dict(
        valid=False,
        msg=dict()
    )
    password = password.strip()
    str_valid = True
    # for c in password:
    #     if c not in valid_str:
    #         str_valid = False
    # confirm_password = confirm_password.strip()
    length_valid = 6 <= len(password) <= 20
    # confirm_valid = password == confirm_password
    result['valid'] = str_valid and length_valid
    msg = result['msg']
    if not str_valid:
        msg['.password-message'] = '输入6-20位密码,只能使用英文字母、下划线及数字'
    if not length_valid:
        msg['.password-message'] = '输入6-20位密码,只能使用英文字母、下划线及数字'
    # if not confirm_valid:
    #     msg['.confirm-message'] = '重复输入的密码'
    return result


def email_valid(email):
    result = dict(
        valid=False,
        msg=dict()
    )
    str_valid = True
    email = email.strip()
    # for c in email:
    #     if c not in email_valid_str:
    #         str_valid =False

    split_email = email.split('@', 1)
    split_valid = len(split_email) == 2
    not_exist = False
    if split_valid and split_email[0] != '' and split_email[1] != '':
        host = split_email[1]
        split_host = host.split('.', 1)
        split_valid = len(split_host) == 2
        if split_valid and split_host[0] != '' and split_host[1] != '':
            u = User.query.filter_by(email=email).first()
            if u is None:
                not_exist = True
    else:
        str_valid = False
    result['valid'] = str_valid and not_exist
    msg = result['msg']
    if not str_valid:
        msg['.email-message'] = '请输入正确的邮箱'
    elif not not_exist:
        msg['.email-message'] = '邮箱已被注册'
    return result


def setting_valid(self, form, message):
    email = form.get('email')
    email_valid = User.email_valid(email, message)
    return email_valid

def change_password_valid(self, form, message):
    old = form.get('old-password')
    new = form.get('new-password')
    confirm = form.get('confirm-password')
    old_valid = old == self.password
    new_valid = User.password_valid(new, confirm, message)
    if not old_valid:
        message['.old-psw-message'] = '请输入当前密码'
    return new_valid and old_valid