from datetime import datetime

from flask import Flask, g, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import current_user, LoginManager
from models import db, timestamp, User
from views.api import main as routes_api
from views.general import main as routes_general
from views.admin import main as routes_admin
from views.post import main as routes_post
from views.user import main as routes_user
from utils.plugin import *

app = Flask(__name__)
manager = Manager(app)
lm = LoginManager()
hostname = 'kaede'

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()
        g.user.save()

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.context_processor
def create_base_data():
    user = g.user
    data = {
        'user': user,
        'hostname': hostname,
        'current_time': timestamp(),
    }
    return data

def register_routes(app):
    app.register_blueprint(routes_general)
    app.register_blueprint(routes_post, url_prefix='/post')
    app.register_blueprint(routes_admin, url_prefix='/admin')
    app.register_blueprint(routes_api, url_prefix='/api')
    app.register_blueprint(routes_user, url_prefix='/user')

def configure_app():
    app.config.from_object('config')
    db.init_app(app)
    lm.init_app(app)
    csrf.init_app(app)
    register_routes(app)
    configure_uploads(app, uploaded_avatars)
    patch_request_class(app, 2 * 1024 * 1024) # 最大2Mb


def configured_app():
    configure_app()
    return app

# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    print('server run')
    app = configured_app()
    config = dict(
        debug = True,
        host = 'localhost',
        port = 3000,
    )
    app.run(**config)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)

@app.errorhandler(404)
def internal_error(error):
    return render_template('base/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('base/500.html'), 500

if __name__ == '__main__':
    configure_manager()
    configure_app()
    manager.run()
