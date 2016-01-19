import datetime
from bson import ObjectId
from mongoengine import EmbeddedDocument, StringField, DateTimeField, IntField
import time

__author__ = 'hezhisu'


class Comment(EmbeddedDocument):
    comment_id = StringField()
    publisher = StringField(required=True)
    publisher_id = StringField(required=True)
    publish_time = IntField(default=time.time()*1000)
    content = StringField(required=True)

