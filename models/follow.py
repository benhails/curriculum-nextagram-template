from models.base_model import BaseModel
from models.user import User
import peewee as pw
from peewee import fn
from playhouse.hybrid import hybrid_property, hybrid_method
from flask import flash
from flask_login import current_user
from enum import Enum


class Follow(BaseModel):
    class FollowStatus(Enum):
        REQUESTED = 1
        REJECTED  = 2
        APPROVED  = 3

    fan = pw.ForeignKeyField(User, backref='idols', on_delete='CASCADE') # unique=False, null=False [already set by default]
    idol = pw.ForeignKeyField(User, backref='fans', on_delete='CASCADE') # unique=False, null=False [already set by default]
    status = pw.IntegerField(default=FollowStatus.APPROVED.value) # unique=False, null=False [already set by default]


    @hybrid_property
    def uid(self):
        return str(self.fan_id) + '-' + str(self.idol_id)

    @uid.expression
    def uid(cls):
        return fn.CONCAT(cls.fan_id, '-', cls.idol_id)



    # def check_is_follower(idol_id):
    #     if Follow.get_or_none(current_user.id == Follow.fan_id and idol_id == Follow.idol_id):
    #         return True
    #     else:
    #         False

    # @hybrid_method
    # def get_post_action(self):
    #     if Follow.get_or_none(current_user.id == Follow.fan_id and user_id == Follow.idol_id):
    #         return 'Delete'

        # should return either
        # {{ url_for('follows.create', idol_id = user.id) }}
        # {{ url_for('follows.delete', ??) }}


    def validate(self):
        if Follow.get_or_none(self.uid == Follow.uid): 
            self.errors.append("You're already following that idol!")
        if str(self.fan_id) == str(self.idol_id):
            self.errors.append("You can't follow yourself!")