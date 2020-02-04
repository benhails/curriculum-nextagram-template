from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.image import Image
from models.user import User
from flask_login import login_user, current_user
from helpers import s3 
from config import S3_BUCKET, S3_LOCATION, S3_IMAGES_FOLDER
from instagram_web.util.helpers import upload_file_to_s3

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('images/new.html')


@images_blueprint.route('/', methods=['POST'])
def create():
    try:
        id = current_user.id
        file = request.files['file']
        blurb = request.form.get('blurb')
        e = upload_file_to_s3(file=file, id=id, folder=S3_IMAGES_FOLDER)
        if e:
            return redirect(url_for('images.new'))
        else:
            Image(blurb=blurb, image=file.filename, user_id=id).save()
            return redirect(url_for('users.show', id=id)) # should probably change this to an images.show page that will show the image that was uploaded
    except: 
        flash("Please add a file!", 'danger')
        return redirect(url_for('images.new'))
        

@images_blueprint.route('/<id>', methods=["GET"])
def show(id):
    pass
    

# use this to show my-feed.
@images_blueprint.route('/my-feed', methods=["GET"])
def index():
    # get all users I follow so I can then extract the images and display them on screen; if I can't do it cleanly in the HTML then process the data further in the model first
    # fan_list = User.get_or_none(User.id == current_user.id).images
    feed = User.get_by_id(current_user.id).where(User.idols.status == 'approved').order_by(User.idols.images.created_at.desc())
    return render_template('images/my-feed.html', feed=feed)


@images_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@images_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
    
