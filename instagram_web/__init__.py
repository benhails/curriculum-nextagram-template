from app import app
import os
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_login import LoginManager, login_required
from models.user import User
from instagram_web.util.helpers import oauth

assets = Environment(app)
assets.register(bundles)

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/images")
app.register_blueprint(sessions_blueprint)
app.register_blueprint(follows_blueprint, url_prefix="/follows")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "sessions.login_new"
login_manager.login_message = "You need to log in to view this page."
login_manager.login_message_category = "danger"


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found_error(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    return render_template('home.html')

# @app.route("/about-us") #i.e. the sort of static pages that get initialised on start but aren't part of a model i.e. don't use DB
# def home():
#     return render_template('home.html')
