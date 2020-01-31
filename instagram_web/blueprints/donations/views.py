from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.donations import Donation
from models.images import Image
from models.user import User
from flask_login import login_user, current_user
from app import gateway
from instagram_web.util.helper import send_email


donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')


@donations_blueprint.route('/<image_id>/donations/new', methods=['GET'])
def new(image_id):
    image = Image.get_by_id(image_id)
    # user_id = request.args.get('user_id') # temp line for customer integration
    # token = gateway.client_token.generate({"customer_id":user_id}) # temp line for customer integration
    token = gateway.client_token.generate() # need to use this afterwards as we're currently not setting up customers for payments
    return render_template('donations/new.html', token=token, image=image)


@donations_blueprint.route('/<image_id>/donations/', methods=['POST'])
def create(image_id):
    nonce_from_the_client = request.form["payment_method_nonce"]
    amount = request.form.get('amount')
    user = request.args.get('user_id')
    result = gateway.transaction.sale({
        "amount": amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
        "submit_for_settlement": True
        }
    })
    if result.is_success:
        donation = Donation(currency="USD", amount=amount, image=image_id, user=user, trans_id=result.transaction.id)
        donation.save()
        user = User.get_by_id(user)
        image = Image.get_by_id(image_id)
        send_email(user, amount, image)
        flash('Your donation has been received. Thank you!', 'success')
    else:
        flash('Something went wrong, please try again!', 'danger')
        
    return redirect(url_for('donations.new', image_id=image_id))
    

@donations_blueprint.route('/<image_id>', methods=["GET"])
def show(image_id):
    pass
    

@donations_blueprint.route('/', methods=["GET"])
def index():
    pass


@donations_blueprint.route('/<image_id>/edit', methods=['GET'])
def edit(image_id):
    pass


@donations_blueprint.route('/<image_id>', methods=['POST'])
def update(image_id):
    pass
    
