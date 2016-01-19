import datetime
import json
from mongoengine import Document, IntField, StringField, DateTimeField, ReferenceField
import time
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'

class Clazz(Document):
    clazz_num = IntField(default=10000)
    clazz_name = StringField(required=True)
    create_time = IntField(default=time.time()*1000)
    member_count = IntField(default=1)
    creator = ReferenceField(User)

    ##生成返回数据
    def json(self):
            data = json.loads(self.to_json())
            creator={}
            creator['phone'] = self.creator.phone
            creator['user_id'] = str(self.creator.id)
            creator['name'] = self.creator.name
            data['creator']=creator
            data['clazz_id']=str(self.id)
            del data['_id']
            return data

