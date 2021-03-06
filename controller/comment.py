from flask import g
from models import Comment
from models import Post


def add(form):
    result = dict(
        success=False,
        message=dict(),
        data=dict()
    )
    valid_msg = form_valid(form)
    valid = valid_msg['valid']
    result['success'] = valid
    result['message'] = valid_msg['msg']
    if valid:
        # form = form.to_dict()
        form['user_id'] = int(g.user.id)
        c = Comment.new(form)
        user = c.post.user
        print(user)
        data = result['data']
        data['comment'] = c.json()
        data['user'] = user.json()
    return result

def form_valid(form):
    result = dict(
        valid=False,
        msg=dict()
    )
    p = Post.query.get(form.get('post_id'))
    valid_post_exist = p is not None
    content = form.get('content', '')
    content = content.strip()
    valid_content_len = 200 >= len(content) >= 1
    message = result['msg']
    if not valid_post_exist:
        message['.comment-message'] = '主题不存在'
    elif not valid_content_len:
        message['.comment-message'] = '内容不能为空'
    result['valid'] = valid_post_exist  and valid_content_len
    return result

# def create_notify(post, sender):
#     notify = {
#         'target_id': post.id,
#         'target_type': TARGET_TYPE.POST,
#         'action': ACTION_TYPE.COMMENT,
#         'sender_id': sender.id,
#         'content': sender.username + '评论了你的文章' + post.title,
#     }
#     notify_service.create_remind(**notify)
#
# def subscribe_comment(comment, user):
#     subscribe = {
#         'user': user,
#         'target_id': comment.id,
#         'target_type': TARGET_TYPE.COMMENT,
#         'reason': REASON_TYPE.COMMENT_POST
#     }
#     notify_service.subscribe(**subscribe)