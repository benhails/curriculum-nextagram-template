from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import login_user, current_user


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    # COULD USE THE BELOW BUT NOT GOOD PRACTICE AS NOT CONTROLLING WHAT'S PASSED TO THE DB
    # data = request.form.to_dict()
    # new_user = User(data)

    # THIS IS A MORE COMPLEX METHOD AND NOT SUITABLE BECAUSE 
    # u = request.form
    # new_user = User(name=u.get('name'), email=u.get('email'), username=u.get('username'), password=generate_password_hash(u['password']))

    # THE SIMPLE WAY IS SHOWN BELOW AND IS BEST FOR RE-USE OF THE VARIABLES
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    new_user = User(name=name, username=username, email=email, password=password)

    if new_user.save():
        user_for_auth = User.get_or_none(User.email==new_user.email)
        login_user(user_for_auth)
        flash("You've signed up Successfully and are now logged in!", 'success')
        return redirect(url_for('users.new')) # (users.show) in the future - just using users.new for testing
    else:
        for error in new_user.errors:
            flash(error, 'danger')
        return render_template('users/new.html', name=name, username=username, email=email, password=password)
    

@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    if User.get_or_none(User.id==id):
        user = User.get_by_id(id)
        if user.id == current_user.id:
            return render_template('users/show.html', name=user.name, username=user.username, email=user.email, id=user.id)
        else:
            return render_template('401.html')
    else:
        return render_template('401.html') # this could potentially be a page not found error as really it's because the id doesn't exist but why give away that the id does exist if we don't have to?
    

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    if User.get_or_none(User.id==id):
        user = User.get_by_id(id)
        if user.id == current_user.id:
            return render_template('users/edit.html', name=user.name, username=user.username, email=user.email)
        else:
            return render_template('401.html')
    else:
        return render_template('401.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    
    pass
