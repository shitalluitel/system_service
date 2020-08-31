from datetime import datetime

import mongoengine as me

# from system_service.api.v1.resources.users.models import User
# from system_service.app import db


class Device(me.Document):
    name = me.StringField(required=True)
    date_created = me.DateTimeField(default=datetime.utcnow, assign=True)
    assigned_to = me.IntField()
