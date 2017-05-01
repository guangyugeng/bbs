from .__init__ import main
from flask import request
import json
from app.controller import user

@main.route('/api/login', methods=['post'])
def login():
    login_form = request.form()
    r = user.login(login_form)
    return json.dumps(r)

@main.route('/api/register', methods=['post'])
def register():
    register_form = request.form()
    r = user.register(register_form)
    return json.dumps(r)
