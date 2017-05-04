from app.models import User
from flask_login import login_user
from functools import wraps
from utils import log
from flask import g

def login_valid(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        form = args[0]
        username = form.get('login_username')
        password = form.get('login_password')
        log(username)
        u = User.query.filter_by(username=username).first()
        log('valid',u)
        valid = u is not None and u.password == password
        log(valid)
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

        username = form.get('register_username')
        nickname = form.get('register_nickname')
        password = form.get('register_password')
        # confirm_password = form.get('confirm')
        email = form.get('register_email')
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
        log(un_valid,pw_valid,e_valid,nn_valid)
        r = dict(
            valid=un_valid and pw_valid and e_valid and nn_valid,
            msg=msg
        )
        args = form, r
        return function(*args, **kwargs)
    return wrapper

def change_info_valid(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        form = args[0]
        nickname = form.get('change_nickname')
        email = form.get('change_email')
        log(nickname)
        # u = User.query.filter_by(nickname=nickname).first()
        # log('valid',u)
        msg = dict()
        if g.user.nickname == nickname:
            nn_valid = True
        else:
            nn_valid_msg = nickname_valid(nickname)
            nn_valid = nn_valid_msg['valid']
            msg.update(nn_valid_msg['msg'])
        if g.user.email == email:
            e_valid = True
        else:
            e_valid_msg = email_valid(email)
            e_valid = e_valid_msg['valid']
            msg.update(e_valid_msg['msg'])
        r = dict(
            valid=e_valid and nn_valid,
            msg=msg
        )
        args = form, r
        return function(*args, **kwargs)
    return wrapper

def change_password_valid(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        form = args[0]
        old = form.get('old-password')

        # u = User.query.filter_by(username=username).first()
        # log('valid',u)
        valid = g.user.password == old
        log(valid)
        r = dict(
            valid=valid,
            msg=dict()
        )
        msg = r['msg']
        if not valid:
            msg['.password-message'] = '当前密码错误'
        args = form, r
        return function(*args, **kwargs)
    return wrapper

@login_valid
def login(form, r=dict):
    if r['valid']:
        log("login")
        db_u = User.query.filter_by(username=form['login_username']).first()
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

@change_info_valid
def change_info(form, r=dict):
    if r['valid']:
        g.user.nickname = form.get('change_nickname')
        g.user.email = form.get('change_email')
        g.user.save()
    return r

@change_password_valid
def change_password(form, r=dict):
    if r['valid']:
        g.user.nickname = form.get('change-nickname')
        g.user.email = form.get('change-email')
        g.user.save()
    return r


def username_valid(username):
    result = dict(
        valid=True,
        msg=dict()
    )
    u = User.query.filter_by(username=username).first()
    if u is not None:
        result['valid'] = False
        result['msg']['.username-message'] = '用户名已被注册'
    # str_valid = True
    # # log(username)
    # username = username.strip()
    # # for c in username:
    # #     if c not in valid_str:
    # #         str_valid = False
    # length_valid = 4 <= len(username) <= 20
    # u = User.query.filter_by(username=username).first()
    # not_exist = u is None
    # result['valid'] = str_valid and length_valid and not_exist
    # # log(type(result['msg']))
    # msg = result['msg']
    # if not str_valid:
    #     msg['.username-message']='输入4-20位用户名,只能使用英文字母、下划线及数字'
    # elif not length_valid:
    #     msg['.username-message']='输入4-20位用户名,只能使用英文字母、下划线及数字'
    # elif not not_exist:
    #     msg['.username-message']= '用户名已存在'
    return result


def nickname_valid(nickname):
    result = dict(
        valid=True,
        msg=dict()
    )
    u = User.query.filter_by(nickname=nickname).first()
    if u is not None:
        result['valid'] = False
        result['msg']['.nickname-message'] = '昵称已被注册'
    #     str_valid = True
    # # log(nickname)
    # # nickname = nickname.strip()
    # # # for c in username:
    # # #     if c not in valid_str:
    # # #         str_valid = False
    # # length_valid = 2 <= len(nickname) <= 20
    # u = User.query.filter_by(nickname=nickname).first()
    # not_exist = u is None
    # result['valid'] = str_valid and length_valid and not_exist
    # # log(type(result['msg']))
    # msg = result['msg']
    # if not str_valid:
    #     msg['.username-message']='输入2-20昵称,只能使用英文字母、下划线及数字'
    # elif not length_valid:
    #     msg['.username-message']='输入2-20昵称,只能使用英文字母、下划线及数字'
    # elif not not_exist:
    #     msg['.username-message']= '昵称已存在'
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
        valid=True,
        msg=dict()
    )
    # str_valid = True
    # # email = email.strip()
    # # for c in email:
    # #     if c not in email_valid_str:
    # #         str_valid =False
    #
    # split_email = email.split('@', 1)
    # split_valid = len(split_email) == 2
    # not_exist = False
    # if split_valid and split_email[0] != '' and split_email[1] != '':
    #     host = split_email[1]
    #     split_host = host.split('.', 1)
    #     split_valid = len(split_host) == 2
    #     if split_valid and split_host[0] != '' and split_host[1] != '':
    u = User.query.filter_by(email=email).first()
    log(u)
    if u is not None:
        result['valid'] = False
        result['msg']['.email-message'] = '邮箱已被注册'
        # not_exist = True
    # else:
    #     str_valid = False
    # result['valid'] =  not_exist
    # msg = result['msg']
    # if not str_valid:
    #     msg['.email-message'] = '请输入正确的邮箱'
    # elif not not_exist:
    #     msg['.email-message'] = '邮箱已被注册'
    return result


