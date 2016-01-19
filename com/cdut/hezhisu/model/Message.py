import datetime
import json
import time
from mongoengine import Document, StringField, DateTimeField, ListField, EmbeddedDocumentField, IntField, ReferenceField, \
    EmbeddedDocumentListField
from com.cdut.hezhisu.model.Attachment import Attachment
from com.cdut.hezhisu.model.Comment import Comment
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'

class Message(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    attachments = ListField(EmbeddedDocumentField(Attachment),required=False)
    read_users = ListField(ReferenceField(User),required=False)
    create_time = IntField(default=time.time()*1000)
    comments = EmbeddedDocumentListField(Comment,required=False)
    publisher = StringField(required=True)
    publisher_id = StringField(required=True)
    clazz_id = StringField(required=True)

    def json(self,is_all):
        data = json.loads(self.to_json())
        data['message_id']=str(self.id)
        del data['_id']
        del data['clazz_id']

        if is_all:
            read_users = []
            for user in self.read_users:
                read_user = {}
                read_user['user_id']=str(user.id)
                read_user['name']=user.name
                read_users.append(read_user)
            data['read_users']=read_users

        else:
            del data['read_users']
            data['read_users_count']=len(self.read_users)
            del data['comments']
            data['comments_count']=len(self.comments)
            del data['attachments']
            data['attachments_count']=len(self.attachments)
        return data