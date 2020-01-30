from models.base_model import BaseModel
from flask import flash
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from helpers import s3
from config import S3_BUCKET, S3_LOCATION, S3_PROFILE_IMAGES_FOLDER
from playhouse.hybrid import hybrid_property

PROFILE_AVATAR_PUBLIC = '/static/images/profile-avatar-public.png'

class User(BaseModel, UserMixin):
    name = pw.CharField(unique=False, null=True, default='')
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
    image = pw.CharField(unique=False, null=True, default='')

    @hybrid_property
    def full_url(self):
        self.image = S3_LOCATION + S3_PROFILE_IMAGES_FOLDER + self.image if self.image else PROFILE_AVATAR_PUBLIC
        return self.image

    # THE BELOW FUNCTION MAY BE NEEDED IF I DIDN'T HAVE A BACK REF
    # def get_user_images(self):
    #     from models.images import Image
    #     return Image.select().where(Image.user_id == self.id)

    def validate(self):
        upper = False
        lower = False
        special = False

        if self.username or not(self.id):
            duplicate_username = User.get_or_none(User.username == self.username)
            if len(self.username)<6:
                self.errors.append('Your username must be at least 6 characters')
            if duplicate_username:
                self.errors.append('That username has already been taken')
        
        if self.email or not(self.id):
            duplicate_email = User.get_or_none(User.email == self.email)
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            valid_email = re.match(email_regex, self.email)
            if duplicate_email:
                self.errors.append('That email has already been registered')
            if not(valid_email):
                self.errors.append('That email address is invalid')

        if self.password or not(self.id):
            for l in self.password:
                if l.isupper():
                    upper = True
                elif l.islower():
                    lower = True
                elif not(l.isalnum()):
                    special = True
            pw_upper_lower_special = upper & lower & special
            # pw_special_character = re.search(r'\W', self.password)
            if len(self.password)<6 or not(pw_upper_lower_special):
                self.errors.append('Your password must be at least 6 characters long and contain an upper case letter, a lower case letter and a special character')
            else:
                self.password = generate_password_hash(self.password)