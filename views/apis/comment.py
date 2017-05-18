from .__init__ import main
from flask import request


@main.route('/comment/add', methods=['post'])
@user_required
def comment_add():
    c_json = request.get_json()
    data = comment.add(c_json)
    return jsonify(data)