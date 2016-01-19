from mongoengine import Q
from com.cdut.hezhisu.main import RedisHelper
from com.cdut.hezhisu.main.RedisHelper import RedisOperation
from com.cdut.hezhisu.model.Clazz import Clazz
from com.cdut.hezhisu.model.Member import Member

__author__ = 'hezhisu'

##发送加班申请
def send_join_class_push(clazz_id,member):
    redis_helper = RedisOperation()
    clazz = Clazz.objects(id=clazz_id).first()
    redis_helper.set_channel('class')
    redis_helper.set_push_type(101)
    push_ids = []
    push_ids.append(str(clazz.creator.id))
    redis_helper.set_push_ids(push_ids)
    push_content_json={}
    push_content_json['classId']=str(clazz.id)
    push_content_json['memberId']=str(member.id)
    push_content_json['content']=member.user.name + "申请加入" + clazz.clazz_name
    redis_helper.set_push_content(push_content_json)
    redis_helper.push()

##同意加班推送
def send_agree_join_class_push(clazz_id,member_id):
    redis_helper = RedisOperation()
    clazz = Clazz.objects(id=clazz_id).first()
    redis_helper.set_channel('class')
    redis_helper.set_push_type(102)
    push_ids = []
    member = Member.objects(id=member_id).first()
    push_ids.append(str(member.user.id))
    redis_helper.set_push_ids(push_ids)
    push_content_json={}
    push_content_json['classId']=str(clazz.id)
    push_content_json['memberId']=str(member.id)
    push_content_json['content']=clazz.creator.name + "老师同意你加入" + clazz.clazz_name
    redis_helper.set_push_content(push_content_json)
    redis_helper.push()

##拒绝加班
def send_refuse_join_class_push(clazz_id,member_id):
    redis_helper = RedisOperation()
    clazz = Clazz.objects(id=clazz_id).first()
    redis_helper.set_channel('class')
    redis_helper.set_push_type(103)
    push_ids = []
    member = Member.objects(id=member_id).first()
    push_ids.append(str(member.user.id))
    redis_helper.set_push_ids(push_ids)
    push_content_json={}
    push_content_json['classId']=str(clazz.id)
    push_content_json['memberId']=str(member.id)
    push_content_json['content']=clazz.creator.name + "老师拒绝你加入" + clazz.clazz_name
    redis_helper.set_push_content(push_content_json)
    redis_helper.push()

def send_publish_message_push(users,message_id):
    redis_helper = RedisOperation()
    redis_helper.set_channel('message')
    redis_helper.set_push_type(201)
    push_ids = []
    for user in users:
        push_ids.append(str(user.id))
    redis_helper.set_push_ids(push_ids)
    push_content_json={}
    push_content_json['messageId']=str(message_id)
    redis_helper.set_push_content(push_content_json)
    redis_helper.push()