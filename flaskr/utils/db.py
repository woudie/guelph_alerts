from mongoengine import *
from datetime import (datetime, timedelta)

class emails(Document):
    email = StringField(required=True)
    expire = StringField(required=True)
    
class courses(Document):
    course = StringField(required=True)
    all_emails = ListField(ReferenceField(emails, reverse_delete_rule=PULL))
