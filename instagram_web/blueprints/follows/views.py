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
    f = {}
    f['fan_id'] = current_user.id
    f['idol_id'] = request.args.get('idol_id')
    f['status'] = 'approved'
    follow = Follow(**f)
    if follow.save():
        flash("You're now following this user", 'success')
    else: 
        for error in follow.errors:
            flash(error, 'danger')
    return redirect(url_for('users.show', id=f.get('idol_id')))
    

# show all users that I follow and all users that follow me
@follows_blueprint.route('/', methods=["GET"])
def index():
    fan_list = User.get_or_none(User.id == current_user.id).images
    # need to make this work for fans and idols if the same is blank/not present
    breakpoint()
    # idol_list = User.get_by_id(current_user.id).idols
    # may need to further process the above results to get exactly what I need for displaying on the page
    # return render_template('follows/index.html', fan_list=fan_list, idol_list=idol_list)
    return render_template('follows/index.html')

# update the status of a follow based on rejection/approval
@follows_blueprint.route('/<follow_id>/update', methods=['POST'])
def update(id):
    pass


# destroy a follow record
@follows_blueprint.route('/<follow_id>/unfollow', methods=['POST'])
def delete(id):
    pass
    

# @follows_blueprint.route('/<id>/follow/new', methods=['GET'])
# def new(id):
#     pass

# @follows_blueprint.route('/<id>', methods=["GET"])
# def show(id):
#     pass

# @follows_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#     pass

