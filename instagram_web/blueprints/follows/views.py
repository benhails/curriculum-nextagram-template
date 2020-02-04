from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models.follow import Follow
from flask_login import current_user
from instagram_web.util.helpers import send_email


follows_blueprint = Blueprint('follows',
                            __name__,
                            template_folder='templates')


# create a follow record
@follows_blueprint.route('/', methods=['POST'])
def create():
    idol_id = request.args.get('idol_id')
    f = {}
    f['fan_id'] = current_user.id
    f['idol_id'] = idol_id
    # status currently using default as defined in model
    follow = Follow(**f)
    if follow.save():
        flash("You're now following this user", 'success')
    else: 
        for error in follow.errors:
            flash(error, 'danger')
    return redirect(url_for('users.show', id=idol_id))
    

# show all users that I follow and all users that follow me
@follows_blueprint.route('/', methods=["GET"])
def index():
    return render_template('follows/index.html')


# update the status of a follow based on rejection/approval
@follows_blueprint.route('/<idol_id>/update', methods=['POST'])
def update(idol_id):
    pass


# destroy a follow record
@follows_blueprint.route('/<idol_id>/unfollow', methods=['POST'])
def delete(idol_id):
    Follow.get_or_none((Follow.idol_id == idol_id) & (Follow.fan_id == current_user.id)).delete_instance()
    flash("You're no longer following this user!", 'success')
    return redirect(url_for('users.show', id=idol_id))
    

# @follows_blueprint.route('/<id>/follow/new', methods=['GET'])
# def new(id):
#     pass

# @follows_blueprint.route('/<id>', methods=["GET"])
# def show(id):
#     pass

# @follows_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#     pass

