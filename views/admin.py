from flask import Blueprint, render_template, flash
from models import Node, Topic
from controller import user

main = Blueprint('admin', __name__)

@main.route('/node')
@user.admin_required
def node_view():
    node_list = Node.user_list()
    topic_list = Topic.user_list()
    return render_template('admin/node.html',
                           node_list=node_list,
                           topic_list=topic_list)

@main.route('/topic')
@user.admin_required
def topic_view():
    data = Topic.user_list()
    if data is not None:
        s = ''
        # log(data)
        for d in data:
            # log(d)
            s += d.name
        flash("topic init success:{}".format(s))
    else:
        flash("topic init fail")
    return render_template('admin/topic.html')
