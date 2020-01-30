from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property
from config import S3_LOCATION, S3_IMAGES_FOLDER


class Image(BaseModel):
    blurb = pw.CharField(unique=False, null=True, default='')
    image = pw.CharField(unique=False, null=False)
    user = pw.ForeignKeyField(User, backref='images', on_delete='CASCADE') # unique=False, null=False [already set by default]

    # Instance method: image_instance.get_url (as property)
    # Class method: Image.select().where(Image.get_url == 'https://www.amazon.com/blalh')
    # NB. Never invoke a hybrid_property
    # NB2. There's not really much point in full_url being a hybrid property as I'll never have the full string in the DB so no need to query based on it 
    @hybrid_property # hybrid because it can be used on a class and an instance
    def full_url(self):
        return S3_LOCATION + S3_IMAGES_FOLDER + self.image

    # instance method
    # img_instance.validate()
    def validate(self):
        pass
    
    # Image.hello()
    # @classmethod
    # def hello():
    #     print('Can be called like this: Image.hello()')