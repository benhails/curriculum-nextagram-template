from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import login_user, current_user
from helpers import s3 
from config import S3_BUCKET, S3_LOCATION

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
    if User.get_or_none(User.id==id):
        user = User.get_by_id(id)
        if user.id == current_user.id:
            image = S3_LOCATION + user.image if user.image else '/static/images/profile-avatar.png'
            return render_template('users/show.html', name=user.name, username=user.username, email=user.email, id=user.id, image=image)
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
    if User.get_or_none(User.id==id):
        user = User.get_by_id(id)
        if user.id == current_user.id:
            return render_template('users/add_image.html', id=id)
        else:
            return render_template('401.html')
    else:
        return render_template('401.html')


def upload_file_to_s3(file, id, acl="public-read"):
    
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        User.update(image=file.filename).where(User.id == id).execute()
        flash('Image successfully uploaded', 'success')

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        flash("Something Happened: ", e)
        return e


@users_blueprint.route('<id>/profile-images/', methods=["POST"])
def profile_images_create(id):
    file = request.files['file']
    e = upload_file_to_s3(file, id)
    if e:
        return redirect(url_for('users.profile_images_new', id=id))
    else:
        return redirect(url_for('users.show', id=id))
