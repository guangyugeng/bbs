from app import db
from datetime import datetime

# from .Base import ModelMin, timestamp
from hashlib import md5
import time
from functools import wraps
from utils import log

ROLE_USER = 0
ROLE_ADMIN = 1



class ModelMin(object):
    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def hidden(self):
        self.hidden = True
        db.session.commit()

    def _update(self):
        db.session.merge(self)
        db.session.commit()

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()


def timestamp():
    return datetime.now()


class User(db.Model, ModelMin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password = db.Column(db.String(120), index = True)
    # role = db.Column(db.SmallInteger, default = ROLE_USER)
    # user_info= db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    posts = db.relationship('Post', lazy='dynamic',cascade="delete, delete-orphan", backref='user')
    comments = db.relationship('Comment', lazy='dynamic',cascade="delete, delete-orphan", backref='user')

    def __init__(self, form):
        # r = self.register_valid(form)
        # if r['valid'] == False:
        #     k,v = r['msg'].popitem()
        #     raise ValueError('msg{}:{}'.format(k,v) )
        self.username = form.get('register_username', '')
        self.password = form.get('register_password', '')
        self.nickname = form.get('register_nickname', '')
        self.email = form.get('register_email', '')

    @staticmethod
    def view(username):
        # data = {}
        user = User.query.filter_by(username=username).first()
        # data['view_user'] = user
        return user.__dict__

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    # def avatar(self, size):
    #     return 'http://www.gravatar.com/avatar/' + md5(self.email.encode(encoding='UTF-8',errors='strict')).hexdigest()+ '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<User %r>' % (self.username)




class Comment(db.Model, ModelMin):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    edited_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    content = db.Column(db.String(200))
    hidden = db.Column(db.Boolean, default=False)
    # replies = db.relationship('Reply', lazy='dynamic',cascade="delete, delete-orphan", backref='comment')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'))

    def __init__(self, form):
        self.created_time = timestamp()
        self.edited_time = timestamp()
        self.user_id = form.get('user_id')
        self.content = form.get('content')
        self.post_id = form.get('post_id')

    def json(self):
        json = {
            'content': self.content,
            'created_time': self.created_time,
        }
        return json


class Topic(db.Model, ModelMin):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    nodes = db.relationship('Node', backref='topic')
    posts = db.relationship('Post', backref='topic')

    def __init__(self, name):
        self.name = name



class Post(db.Model, ModelMin):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    edited_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    title = db.Column(db.String(30))
    content = db.Column(db.String(1000))
    hidden = db.Column(db.Boolean, default=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id', ondelete='CASCADE'))
    comments = db.relationship('Comment', lazy='dynamic',cascade="delete, delete-orphan", backref='post')

    def __init__(self, form):
        self.created_time = timestamp()
        self.edited_time = timestamp()
        self.user_id = form.get('user_id', '')
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.node_id = form.get('node_id')
        self.topic_id = form.get('topic_id')

    def update(self, form):
        self.edit_time = timestamp()
        self.title = form.get('title')
        self.content = form.get('content')
        self.node_id = form.get('node_id')
        self.topic_id = form.get('topic_id')
        self._update()

    def permission_valid(self, u):
        return u.username == self.user.username



class Node(db.Model, ModelMin):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))
    posts = db.relationship('Post', lazy='dynamic',cascade="delete, delete-orphan", backref='node')
    hidden = db.Column(db.Boolean, default=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id', ondelete='CASCADE'))

    def __init__(self, form):
        self.name = form.get('name')
        self.description = form.get('description', '')
        self.topic_id = form.get('topic_id')

    # @classmethod
    # def new(cls, form):
    #     node = cls(form)
    #     node.save()
    #
    # @classmethod
    # def user_list(cls):
    #     data = {}
    #     node_list = Node.query.filter_by(hidden=False)
    #     data['node_list'] = node_list

    def json(self):
        r = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return r