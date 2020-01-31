from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import login_user, logout_user, current_user
from instagram_web.util.helpers import oauth


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/login', methods=["GET"])
def login_new():
    return render_template('sessions/login.html')


@sessions_blueprint.route('/', methods=["POST"])
def login_create(): # should really be login_create
    user_for_auth = User.get_or_none(User.email==request.form.get('email')) # captures User.id of the username if it exists
    if user_for_auth:
        password_to_check = request.form['password']
        hashed_password = user_for_auth.password
        result = check_password_hash(hashed_password, password_to_check) # this function return True or False to result
        if result:
            login_user(user_for_auth) # let flask login take over
            # session["user_id"] = user_for_auth.id # example if not using flask login
            flash('You are now logged in', 'success')
            return redirect('/')
        else:
            flash('Password is incorrect', 'danger')
    else:
        flash('That email address has not been registered', 'danger')

    return render_template('sessions/login.html', email=request.form['email'])


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)


@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash('You are now logged in', 'success')
        return redirect('/')
    else:
        flash('That user does not exist', 'danger')
        return redirect(url_for('sessions.login_new'))


@sessions_blueprint.route('/logout', methods=["POST"])
def login_destroy():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))
