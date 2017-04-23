from datetime import datetime
from app import db


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
