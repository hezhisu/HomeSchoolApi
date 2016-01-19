import threading
import urllib
from bson import ObjectId
from flask import request
from flask_restplus import Resource
from mongoengine import Q
import time
from com.cdut.hezhisu.main.Push import send_join_class_push, send_agree_join_class_push, \
    send_refuse_join_class_push
from com.cdut.hezhisu.model.Clazz import Clazz
from com.cdut.hezhisu.model.Member import Member
from com.cdut.hezhisu.model.Message import Message
from com.cdut.hezhisu.model.Student import Student
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'

class ClazzBiz(object):



    def __init__(self,api,ns):
        response={}
        create_clazz_parser = api.parser()
        create_clazz_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='form')
        create_clazz_parser.add_argument('clazz_name', type=str, required=True, help='班级名称', location='form')

        @ns.route('')
        class CreateClazzResource(Resource):
            @api.doc(parser=create_clazz_parser)
            def post(self):
                '''创建班级 '''
                user_id = request.form.get('user_id')
                clazz_name = request.form.get('clazz_name')
                clazz = Clazz.objects.order_by('-clazz_num').first()
                if clazz == None:
                    clazz = Clazz()
                    clazz.creator = User.objects(id=user_id).first()
                    clazz.clazz_name = clazz_name
                    clazz.create_time = time.time()*1000
                    clazz.save()
                    ##添加成员
                    member = Member()
                    member.clazz_id = str(clazz.id)
                    member.user = clazz.creator
                    member.user_type = 1
                    member.is_creator = True
                    member.status = 1
                    member.save()


                    response['code']=200
                    response['msg']='创建班级成功'
                    response['data']=clazz.json()
                else:
                    clazz_new = Clazz()
                    clazz_new.creator = User.objects(id=user_id).first()
                    clazz_new.clazz_name = clazz_name
                    clazz_new.clazz_num = clazz.clazz_num + 1
                    clazz_new.create_time = time.time()*1000
                    clazz_new.save()

                    ##添加成员
                    member = Member()
                    member.clazz_id = str(clazz_new.id)
                    member.user = clazz_new.creator
                    member.user_type = 1
                    member.is_creator = True
                    member.status = 1

                    member.save()

                    response['code']=200
                    response['msg']='创建班级成功'
                    response['data']=clazz_new.json()
                return response

        @ns.route('/<string:clazz_id>')
        class GetClazzResource(Resource):
            def get(self,clazz_id):
                '''获取班级信息'''
                response['code']=200
                clazz = Clazz.objects(id=clazz_id).all().first()

                response['data']=clazz.json()
                response['msg']='获取班级信息成功'
                return response

        add_member_parser = api.parser()
        add_member_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='form')
        add_member_parser.add_argument('user_type', type=int, required=True, help='身份(0是家长,1是老师)', location='form')
        add_member_parser.add_argument('student_id', type=int, required=False, help='孩子ID', location='form')

        find_clazz_parser = api.parser()
        find_clazz_parser.add_argument('phone', type=str,required=True, help='创建者手机号',location='query')
        @ns.route('/find')
        class FindClazzResource(Resource):

            @api.doc(parser=find_clazz_parser)
            def get(self):
                '''查找班级'''
                response['code']=200
                phone = request.args.get('phone','')
                clazzes = Clazz.objects(creator=User.objects(phone=phone).first()).all()
                clazzes_json = []
                for clazz in clazzes:
                    clazzes_json.append(clazz.json())

                response['data']=clazzes_json
                response['msg']='查找班级成功'
                return response

        add_member_parser = api.parser()
        add_member_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='form')
        add_member_parser.add_argument('user_type', type=int, required=True, help='身份(0是家长,1是老师)', location='form')
        add_member_parser.add_argument('student_id', type=int, required=False, help='孩子ID', location='form')

        @ns.route('/<string:clazz_id>/member')
        class AddMember(Resource):
            @api.doc(parser=add_member_parser)
            def post(self,clazz_id):
                '''申请加班'''
                user_id = request.form.get('user_id')
                user_type = int(request.form.get('user_type'))
                student_id = request.form.get('student_id')
                response['code']=200
                response['msg']='申请加班成功'
                if user_type == 1:
                    member = Member.objects(Q(clazz_id=clazz_id) & Q(user=ObjectId(user_id)) &
                                            Q(status=2)).first()
                    if member:
                        threading.Thread(target=send_join_class_push, args=(clazz_id,member)).start()
                        return response
                else:
                    member = Member.objects(Q(clazz_id=clazz_id) & Q(user=ObjectId(user_id))
                                            & Q(student=ObjectId(student_id)) & Q(status=2)).first()
                    if member:
                        threading.Thread(target=send_join_class_push, args=(clazz_id,member)).start()
                        return response

                member = Member()
                member.user = User.objects(id=user_id).first()
                member.clazz_id = clazz_id
                member.user_type = user_type
                member.status = 2
                if student_id != None:
                    member.student = Student.objects(id=student_id).first()
                member.is_creator=False
                member.save()
                threading.Thread(target=send_join_class_push, args=(clazz_id,member)).start()


                return response

        update_member_parser = api.parser()
        update_member_parser.add_argument('is_agree', type=int, required=True, help='1是同意,0是拒绝',location='form')
        @ns.route('/<string:clazz_id>/member/<string:member_id>')
        class UpdateMemberResource(Resource):

            @api.doc(parser=update_member_parser)
            def put(self,member_id,clazz_id):
                '''同意或拒接加班申请'''
                is_agree = int(request.form.get('is_agree'))
                response['code']=200
                if is_agree == 1:
                    Member.objects(id=member_id).update(status=1)
                    Clazz.objects(id=clazz_id).update(inc__member_count=1)
                    response['msg']='老师同意申请加班'
                    threading.Thread(target=send_agree_join_class_push, args=(clazz_id,member_id)).start()

                else:
                    threading.Thread(target=send_refuse_join_class_push, args=(clazz_id,member_id)).start()
                    response['msg']='老师拒绝申请加班'
                return response


        @ns.route('/<string:clazz_id>/members')
        class GetClassMembersResource(Resource):
            def get(self,clazz_id):
                '''获取班级成员列表'''
                members = Member.objects(clazz_id=clazz_id).exclude('status').all()
                response['code'] = 200
                response['msg']='班级列表'
                items=[]
                for member in members:
                    item = member.json()
                    items.append(item)
                response['data']=items
                return response

        get_class_message_parser = api.parser()
        get_class_message_parser.add_argument('time', type=int, required=True, help="时间戳", location='query')
        @ns.route('/<string:clazz_id>/messages')
        class GetClassMessagesResource(Resource):
            @api.doc(parser=get_class_message_parser)
            def get(self,clazz_id):
                '''根据时间戳获取班级消息列表'''
                time = int(request.args.get('time','0'))
                messages = None
                if time:
                    messages = Message.objects(Q(create_time__lt=time) & Q(clazz_id=clazz_id)).order_by('-create_time')[:5]
                else:
                    messages = Message.objects(clazz_id=clazz_id).order_by('-create_time')[:10]
                response={}
                response['code']=200
                messages_json=[]
                for message in messages:
                    messages_json.append(message.json(False))
                response['data']=messages_json
                return  response





