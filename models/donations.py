from models.base_model import BaseModel
from models.user import User
from models.images import Image
import peewee as pw
from money.money import Money
from money.currency import Currency


class Donation(BaseModel):
    user = pw.ForeignKeyField(User, backref='donations') # unique=False, null=False [already set by default]
    image = pw.ForeignKeyField(Image, backref='donations') # unique=False, null=False [already set by default]
    currency = pw.FixedCharField(max_length=3) # null=False [already set by default]
    amount = pw.DecimalField(rounding=None) # null=False [already set by default]
    trans_id = pw.FixedCharField(unique=True) # null=False [already set by default]

    # THE FOLLOWING IS PSEUDO CODE FOR USING MULTIPLE CURRENCIES WITH https://github.com/vimeo/py-money
    # currencies = Currency._member_names_
    # amount = input form amount
    # currency = input form currency
    # try:
    #   m = Money(amt, Currency._member_map_.get(curr))

    #  except: 
    #      flash('your value is not valid for that currency')
