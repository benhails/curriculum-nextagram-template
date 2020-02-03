from models.base_model import BaseModel
from models.user import User
import peewee as pw
from playhouse.hybrid import hybrid_property


class Follow(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols', on_delete='CASCADE') # unique=False, null=False [already set by default]
    idol = pw.ForeignKeyField(User, backref='fans', on_delete='CASCADE') # unique=False, null=False [already set by default]
    status = pw.CharField() # unique=False, null=False [already set by default] # requested, rejected, approved

    def validate(self):
        pass