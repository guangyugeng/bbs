from app import db
from .Base import ModelMin, timestamp


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