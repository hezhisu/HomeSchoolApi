import json
from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField
from com.cdut.hezhisu.model.Student import Student
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'
class Member(Document):
    clazz_id = StringField(required=True)
    user = ReferenceField(User)
    user_type = IntField(required=True)
    is_creator = BooleanField(required=True)
    student = ReferenceField(Student, required=False)

    ## 1:已经在班级里; 2:等待验证; 0:为加入
    status = IntField(required=True)

    def json(self):
        data = json.loads(self.to_json())
        user={}
        user['phone'] = self.user.phone
        user['user_id'] = str(self.user.id)
        user['name'] = self.user.name
        data['user']=user
        data['member_id']=str(self.id)
        if self.student != None:
            student = self.student.json()
            del student['user']
            data['student']=student
        del data['_id']
        return data