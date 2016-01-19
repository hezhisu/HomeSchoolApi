import json
from mongoengine import Document, ReferenceField, StringField
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'
class Student(Document):
    user = ReferenceField(User, required=True)
    student_name = StringField(required=True)
    identify = StringField(required=True)


    def json(self):
        data={}
        data=json.loads(self.to_json())
        data['student_id'] = str(self.id)
        del data['_id']
        user = self.user
        data_user={}
        data_user['user_id'] = str(user.id)
        data_user['name']=user.name
        data_user['phone']=user.phone
        data['user']=data_user
        return data
