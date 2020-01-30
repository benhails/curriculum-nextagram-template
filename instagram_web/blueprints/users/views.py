from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.images import Image
from instagram_web.util.helper import upload_file_to_s3
from flask_login import login_user, current_user
from helpers import s3
from config import S3_BUCKET, S3_LOCATION, S3_PROFILE_IMAGES_FOLDER # only here temp

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
    confirm_password = request.form.get('confirm_password')
    new_user = User(name=name, username=username, email=email, password=password)
    if password == confirm_password:
        if new_user.save():
            user_for_auth = User.get_or_none(User.email==new_user.email)
            login_user(user_for_auth)
            flash("You've signed up Successfully and are now logged in!", 'success')
            return redirect(url_for('users.show', id=user_for_auth.id)) # (users.show) in the future - just using users.new for testing
        else:
            for error in new_user.errors:
                flash(error, 'danger')
    else:
        flash("Passwords don't match", 'danger')

    return render_template('users/new.html', name=name, username=username, email=email, password=password, confirm_password=confirm_password)


@users_blueprint.route('/<id>', methods=["GET"])
def show(id):
    user = User.get_or_none(User.id==id)
    if user:
        return render_template('users/show.html', user=user)
    else:
        return render_template('404.html')
    

@users_blueprint.route('/', methods=["GET"])
def index():
    user_list = User.select()
    return render_template('users/index.html', user_list=user_list)


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_or_none(User.id==id)
    if user:
        if user.id == current_user.id:
            return render_template('users/edit.html', name=user.name, username=user.username, email=user.email, id=user.id)
        else:
            return render_template('401.html')
    else:
        return render_template('401.html')


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    c = User.get_by_id(id)

    u_name = request.form.get('name')
    u_email = request.form.get('email')
    u_username = request.form.get('username')
    u_password = request.form.get('password')
    u_confirm_password = request.form.get('confirm_password')

    user_dict = {}
    
    user_dict['name'] = u_name
    user_dict['image'] = c.image
    if u_email != c.email:
        user_dict['email'] = u_email
    if u_username != c.username:
        user_dict['username'] = u_username
    if u_password:
        user_dict['password'] = u_password 

    updated_user = User(id=id, **user_dict)
    if u_password == u_confirm_password and u_username and u_email:
        if updated_user.save():
            flash("Your details have been successfully updated!", 'success')
            return redirect(url_for('users.edit', id=id))
        else:
            for error in updated_user.errors: # can change to "<br>.join(updated_user.errors)" or thereabouts rather than using the for loop
                flash(error, 'danger')
    else:
        flash("Passwords don't match or required information is missing", 'danger')

    return render_template('users/edit.html', id=id, name=u_name, username=u_username, email=u_email, password=u_password, confirm_password=u_confirm_password)
    
   
@users_blueprint.route('<id>/profile-images/add', methods=["GET"])
def profile_images_new(id):
    user = User.get_or_none(User.id==id)
    if user:
        if user.id == current_user.id:
            return render_template('users/add_image.html', id=id)
        else:
            return render_template('401.html')
    else:
        return render_template('401.html')


@users_blueprint.route('<id>/profile-images/', methods=["POST"])
def profile_images_create(id):
    try:
        file = request.files['file']
        e = upload_file_to_s3(file=file, id=id, folder=S3_PROFILE_IMAGES_FOLDER)
        if e:
            return redirect(url_for('users.profile_images_new', id=id))
        else:
            User.update(image=file.filename).where(User.id == id).execute()
            return redirect(url_for('users.show', id=id))
    except: 
        flash("Please add a file!", 'danger')
        return redirect(url_for('users.profile_images_new', id=id))
