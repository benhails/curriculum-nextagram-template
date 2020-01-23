from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import check_password_hash
from models.user import User


profile_images_blueprint = Blueprint('profile_images',
                            __name__,
                            template_folder='templates')


@profile_images_blueprint.route('<id>/profile-images/add', methods=["GET"])
def profile_images_new(id):
    return render_template('profile_images/add.html', id=id)


@profile_images_blueprint.route('<id>/profile-images/', methods=["POST"])
def profile_images_create(id):
    return redirect(url_for('users.show', id=id))
