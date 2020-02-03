from models.base_model import BaseModel
from models.user import User
import peewee as pw
from peewee import fn
from playhouse.hybrid import hybrid_property
from flask import flash


class Follow(BaseModel):
    fan = pw.ForeignKeyField(User, backref='idols', on_delete='CASCADE') # unique=False, null=False [already set by default]
    idol = pw.ForeignKeyField(User, backref='fans', on_delete='CASCADE') # unique=False, null=False [already set by default]
    status = pw.CharField() # unique=False, null=False [already set by default] # requested, rejected, approved


    @hybrid_property
    def uid(self):
        return str(self.fan_id) + '-' + str(self.idol_id)

    @uid.expression
    def uid(cls):
        return fn.CONCAT(cls.fan_id, '-', cls.idol_id)

    


    def validate(self):
        if Follow.get_or_none(self.uid == Follow.uid): 
            self.errors.append("You're already following that idol!")
        if str(self.fan_id) == str(self.idol_id):
            self.errors.append("You can't follow yourself!")