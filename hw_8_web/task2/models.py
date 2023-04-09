from mongoengine import Document
from mongoengine.fields import StringField, BooleanField


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    is_sent = BooleanField(default=False)
    preferred_contact_method = StringField(choices=["email", "sms"], default="email")
    address = StringField()
    