from flask import Blueprint, render_template, g, abort, flash, request
from flask_login import login_required
from app.models import Node, Topic
from app.controller import post
from app.forms import AddPostForm

main = Blueprint('post', __name__)

@main.route('/new')
@login_required
def new():
    node_list = Node.user_list()
    form = AddPostForm()
    return render_template('post/add_post.html', form=form)

@main.route('/<int:post_id>')
def view(post_id):
    comment_page = request.args.get('page', '1')
    data = post.view(post_id, comment_page)
    return render_template('post/post.html', user=g.user, **data)

@main.route('/edit/<int:post_id>')
def edit(post_id):
    data = post.edit(post_id)
    form = AddPostForm()
    form.content.data = data['post'].content
    return render_template('post/edit_post.html',
                           form=form,
                           **data)

@main.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post.delete(post_id)

