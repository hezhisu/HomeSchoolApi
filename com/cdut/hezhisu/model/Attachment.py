from mongoengine import EmbeddedDocument, IntField, StringField

__author__ = 'hezhisu'
class Attachment(EmbeddedDocument):
    width = IntField(required=True)
    height = IntField(required=True)
    url = StringField(required = True)