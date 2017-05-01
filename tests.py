#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Topic, Node, Comment, Post
# from app.models.Topic import Topic
# from app.models.Node import Node
# from app.models.Post import Post
# from app.models.Comment import Comment
from datetime import datetime, timedelta
from app.controller.user import register, login
from utils import log


class TestModel(unittest.TestCase):
    form1 = {
        'nickname' : 'john',
        'email' : 'john@example.com',
        'username' : 'mynameisvalid1',
        'password' : 'mypasswordvalid1'
    }
    form2 = {
        'nickname' : 'susan',
        'email' : 'susan@example.com',
        'username' : 'no',
        'password' : 'mypasswordvalid'
    }
    form4 = {
        'nickname' : 'david',
        'email' : 'e4@example.com',
        'username' : 'mynameisvalid4',
        'password' : 'no'
    }
    form5 = {
        'nickname' : '小明',
        'email' : '772815697@qq.com',
        'username' : 'guangyugeng',
        'password' : '123456'
    }
    form6 = {
        'nickname' : '6',
        'email' : 'e6@example.com',
        'username' : 'mynameisvalid4',
        'password' : 'mypasswordvalid'
    }
    form7 = {
        'nickname' : 'nick7',
        'email' : 'nick7@example.com',
        'username' : 'mynameisvalid7',
        'password' : 'mypasswordvalid1'
    }
    def setUp(self):
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.secret_key = 'secret key'
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/bbs'
        db.create_all()

    def tearDown(self):
        db.drop_all()

    # def test_avatar(self):
    #     # create a user
    #     u = User(self.form1)
    #     avatar = u.avatar(128)
    #     expected = 'http://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6'
    #     assert avatar[0:len(expected)] == expected

    def test_register(self):
        assert register(self.form1)['valid'] == True
        # assert register(self.form1)['valid'] == True
        assert register(self.form2)['valid'] == False
        assert register(self.form4)['valid'] == False
        assert register(self.form5)['valid'] == True
        assert register(self.form6)['valid'] == False

    def test_login(self):
        assert register(self.form1)['valid'] == True
        assert register(self.form5)['valid'] == True
        assert login(self.form1)['valid'] == True
        assert login(self.form5)['valid'] == True
        assert login(self.form6)['valid'] == False

    def test_user_view(self):
        u = User(self.form7)
        u.save()
        # log(self.form7.items() and u.view(u.username).__dict__.items(),'view')
        view_dict = u.view(u.username)
        for k, v in self.form7.items():
            if k != 'confirm':
                assert view_dict[k] == view_dict[k]

    def test_topic(self):
        topic1 = Topic('Geek')
        topic2 = Topic('游戏')
        topic1.save()
        topic2.save()

    def test_node(self):
        node_form1 = {'topic_id':1,'name':'程序员', 'description':'While code monkeys are not eating bananas, they\'re coding.'}
        node_form2 = {'topic_id':1,'name':'python', 'description':' 这里讨论各种 Python 语言编程话题，也包括 Django，Tornado 等框架的讨论。这里是一个能够帮助你解决实际问题的地方。 '}
        node_form3 = {'topic_id':2,'name':'英雄联盟', 'description': 'League of Legends (LoL) is a multiplayer online battle arena video game. '}
        node_form4 = {'topic_id':2,'name':'Steam', 'description':' Delivers a range of games straight to a computer\'s desktop. '}
        # topic1 = Topic('Geek')
        # topic2 = Topic('游戏')
        # topic1.save()
        # topic2.save()
        node1_1 = Node(node_form1)
        node1_2 = Node(node_form2)
        node2_1 = Node(node_form3)
        node2_2 = Node(node_form4)
        node1_1.save()
        node1_2.save()
        node2_1.save()
        node2_2.save()
        nodes1 = Node.query.filter_by(topic_id=1).all()
        nodes2 = Node.query.filter_by(topic_id=2).all()
        for n1 in nodes1:
            assert n1.id == node1_1.id or n1.id == node1_2.id
        for n2 in nodes2:
            assert n2.id == node2_1.id or n2.id == node2_2.id

    def test_post(self):
        post_form1 = {'user_id':1,
                      'title':'test title',
                      'content':'test content',
                      'node_id':1,
                      'topic_id':1}
        post_form2 = {'user_id':2,
                      'title':'test title',
                      'content':'test content',
                      'node_id':2,
                      'topic_id':2}
        post_update_form1 = {'title':'test1 title',
                      'content':'test1 content',
                      'node_id':1,
                      'topic_id':1}
        post_update_form2 = {'title':'test2 title',
                      'content':'test2 content',
                      'node_id':2,
                      'topic_id':2}
        post1 = Post(post_form1)
        post1.save()
        post2 = Post(post_form2)
        post2.save()
        post1.update(post_update_form1)
        post2.update(post_update_form2)
        assert post1.title == 'test1 title'

    def test_comment(self):
        comment_form1 = {'user_id':1,
                         'post_id':1,
                         'content':'test1 comment'}
        comment_form2 = {'user_id':2,
                         'post_id':2,
                         'content':'test2 comment'}
        comment1 = Comment(comment_form1)
        comment2 = Comment(comment_form2)
        assert comment1.content == 'test1 comment'
        assert comment2.content == 'test2 comment'

        # log(post1.title)

        # assert self.form7.items() and u.view(u.username).__dict__.items() == self.form7.items()
        # create a user and write it to the database
        # u = User(self.form1)
        # db.session.add(u)
        # db.session.commit()
        # nickname = User.make_unique_nickname('john')
        # assert nickname != 'john'
        # # make another user with the new nickname
        # nickname2 = User.make_unique_nickname('john')
        # self.form1['nickname'] = nickname2
        # self.form1['email'] = 'susan@example.com'
        # self.form1['username'] = 'myname 2'
        # # print('sds',nickname2,nickname)
        # u = User(self.form1)
        # db.session.add(u)
        # db.session.commit()
        # # nickname2 = User.make_unique_nickname('john')
        # assert nickname2 != 'john'
        # assert nickname2 == nickname

    # def test_follow(self):
    #     u1 = User(self.form1)
    #     u2 = User(self.form2)
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     assert u1.unfollow(u2) == None
    #     u = u1.follow(u2)
    #     db.session.add(u)
    #     db.session.commit()
    #     assert u1.follow(u2) == None
    #     assert u1.is_following(u2)
    #     assert u1.followed.count() == 1
    #     assert u1.followed.first().nickname == 'susan'
    #     assert u2.followers.count() == 1
    #     assert u2.followers.first().nickname == 'john'
    #     u = u1.unfollow(u2)
    #     assert u != None
    #     db.session.add(u)
    #     db.session.commit()
    #     assert u1.is_following(u2) == False
    #     assert u1.followed.count() == 0
    #     assert u2.followers.count() == 0
    #
    # def test_follow_posts(self):
    #     # make four users
    #     u1 = User(self.form1)
    #     u2 = User(self.form2)
    #     u3 = User(self.form3)
    #     u4 = User(self.form4)
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     # make four posts
    #     utcnow = datetime.utcnow()
    #     p1 = Post(body = "post from john", author = u1, timestamp = utcnow + timedelta(seconds = 1))
    #     p2 = Post(body = "post from susan", author = u2, timestamp = utcnow + timedelta(seconds = 2))
    #     p3 = Post(body = "post from mary", author = u3, timestamp = utcnow + timedelta(seconds = 3))
    #     p4 = Post(body = "post from david", author = u4, timestamp = utcnow + timedelta(seconds = 4))
    #     db.session.add(p1)
    #     db.session.add(p2)
    #     db.session.add(p3)
    #     db.session.add(p4)
    #     db.session.commit()
    #     # setup the followers
    #     u1.follow(u1) # john follows himself
    #     u1.follow(u2) # john follows susan
    #     u1.follow(u4) # john follows david
    #     u2.follow(u2) # susan follows herself
    #     u2.follow(u3) # susan follows mary
    #     u3.follow(u3) # mary follows herself
    #     u3.follow(u4) # mary follows david
    #     u4.follow(u4) # david follows himself
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.add(u3)
    #     db.session.add(u4)
    #     db.session.commit()
    #     # check the followed posts of each user
    #     f1 = u1.followed_posts().all()
    #     f2 = u2.followed_posts().all()
    #     f3 = u3.followed_posts().all()
    #     f4 = u4.followed_posts().all()
    #     assert len(f1) == 3
    #     assert len(f2) == 2
    #     assert len(f3) == 2
    #     assert len(f4) == 1
    #     assert f1 == [p4, p2, p1]
    #     assert f2 == [p3, p2]
    #     assert f3 == [p4, p3]
    #     assert f4 == [p4]
#
# class TestPosts(unittest.TestCase):
#     def test_topic_node(self):
#         node_form1 = {'id':'1','name':'程序员', 'description':'While code monkeys are not eating bananas, they\'re coding.'}
#         node_form2 = {'id':'1','name':'python', 'description':' 这里讨论各种 Python 语言编程话题，也包括 Django，Tornado 等框架的讨论。这里是一个能够帮助你解决实际问题的地方。 '}
#         node_form3 = {'id':'2','name':'英雄联盟', 'description': 'League of Legends (LoL) is a multiplayer online battle arena video game. '}
#         node_form4 = {'id':'2','name':'Steam', 'description':' Delivers a range of games straight to a computer\'s desktop. '}
#         topic1 = Topic('Geek')
#         topic2 = Topic('游戏')
#         topic1.save()
#         topic2.save()
#         node1_1 = Node(node_form1)
#         node1_2 = Node(node_form2)
#         node2_1 = Node(node_form3)
#         node2_2 = Node(node_form4)
#         node1_1.save()
#         node1_2.save()
#         node2_1.save()
#         node2_2.save()
#         nodes1 = Node.query.filter_by(topic_id=topic1.id).all()
#         nodes2 = Node.query.filter_by(topic_id=topic2.id).all()
#         for n1 in nodes1:
#             assert n1.id == node1_1.id or n1.id == node1_2
#         for n2 in nodes2:
#             assert n2.id == node2_1.id or n2.id == node2_2


if __name__ == '__main__':
    unittest.main()