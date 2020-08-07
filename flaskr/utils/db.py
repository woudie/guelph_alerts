import mongoengine as me
from datetime import datetime

class emails(me.Document):
    email = me.StringField(required=True)
    created = me.DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            {'fields': ['created'], 'expireAfterSeconds': 30}
        ]
    }
    
class courses(me.Document):
    course = me.StringField(required=True)
    all_emails = me.ListField(me.ReferenceField(emails, reverse_delete_rule=me.CASCADE))