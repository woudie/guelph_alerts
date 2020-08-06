import mongoengine as me

class emails(me.Document):
    email = me.StringField(required=True)
    
class courses(me.Document):
    course = me.StringField(required=True)
    all_emails = me.ListField(me.ReferenceField(emails))
