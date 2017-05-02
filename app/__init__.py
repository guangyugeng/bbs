from flask import Flask, g
# from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from app.views.frontend import frontend
from flask_wtf.csrf import CsrfProtect
from datetime import datetime


csrf = CsrfProtect()


app = Flask(__name__)
csrf.init_app(app)


app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
# lm.login_view = 'login'
# Install our Bootstrap extension
# Bootstrap(app)

# Our application uses blueprints as well; these go well with the
# application factory. We already imported the blueprint, now we just need
# to register it:
# app.register_blueprint(frontend)
from app.views.general import main as general
from app.views.api import main as api
from app.views.user import main as user

app.register_blueprint(general)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(user, url_prefix='/user')
# Because we're security-conscious developers, we also hard-code disabling
# the CDN support (this might become a default in later versions):
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# We initialize the navigation as well
# nav.init_app(app)


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()
        g.user.save()


# app.config.from_object('config')
# CsrfProtect(app)


# if not app.debug:
#     import logging
#     from logging.handlers import RotatingFileHandler
#     file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
#     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('bbs startup')

