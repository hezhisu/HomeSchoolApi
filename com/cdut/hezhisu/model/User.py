from bson import ObjectId
from mongoengine import Document, StringField, IntField, ReferenceField

__author__ = 'hezhisu'
#用户model
class User(Document):
    phone = StringField(required=True)
    password = StringField(required=True)
    name = StringField(required=True)
    role_type = IntField(required=True,default=-1)