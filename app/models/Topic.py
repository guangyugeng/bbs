from app import db
from .Base import ModelMin, timestamp


class Topic(db.Model, ModelMin):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    nodes = db.relationship('Node', backref='topic')
    posts = db.relationship('Post', backref='topic')

    def __init__(self, name):
        self.name = name

    # def node(self):
