from .__init__ import main
from flask import request
import json
from app.controller import user


@main.route('/comment/add', methods=['post'])
@user_required
def comment_add():
    c_json = request.get_json()
    data = comment.add(c_json)
    return jsonify(data)