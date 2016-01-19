import json
from bson import ObjectId
from flask import request
from flask_restplus import Resource
from mongoengine import Q
from com.cdut.hezhisu.model.Clazz import Clazz
from com.cdut.hezhisu.model.Member import Member
from com.cdut.hezhisu.model.Student import Student
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'
class UserBiz(object):
    def __init__(self,api,ns):
        response ={}
        parser_modify_info = api.parser()
        parser_modify_info.add_argument('role_type', type=int, required=False, help='身份(0是家长,1是老师)', location='form')
        parser_modify_info.add_argument('name', type=str, required=False, help='姓名', location='form')
        @ns.route('/<string:user_id>')
        class ModifyResource(Resource):
            @api.doc(parser=parser_modify_info)
            def put(self,user_id):
                '''更新用户信息'''
                role_type = request.form.get('role_type')
                name = request.form.get('name')
                user = User.objects(id=user_id).first()
                if role_type != None:
                    user.role_type = role_type
                    user.update(role_type=role_type)
                if name!= None:
                    user.name = name
                    user.update(name=name)

                response['code']=200
                response['msg']='更新成功'
                response['data']= json.loads(user.to_json())
                return response

        parser_get_all_class = api.parser()
        parser_get_all_class.add_argument('user_type', type=int, required=True, help='身份(0是家长,1是老师)', location='query')
        @ns.route('/<string:user_id>/clazzs')
        class GetAllClazzByUserResource(Resource):
            @api.doc(parser=parser_get_all_class)
            def get(self,user_id):
                '''获取用户所在班级信息'''
                response['code']=200
                user_type = int(request.args.get('user_type'))
                items = []
                if user_type == 1:
                    members = Member.objects(Q(user=ObjectId(user_id)) & Q(user_type=user_type) & Q(status=1))
                    for member in members:
                        clazzs = Clazz.objects(id=member.clazz_id).all()
                        for clazz in clazzs:
                            item  = clazz.json()
                            item['is_creator']=member.is_creator
                            del item['creator']
                            items.append(item)
                else:
                    students = Student.objects(user=ObjectId(user_id)).all()
                    for student in students:
                        members = Member.objects(Q(user=ObjectId(user_id)) & Q(student=student.id) & Q(status=1))
                        clazzs_json = []
                        for member in members:
                            clazzs = Clazz.objects(id=member.clazz_id).all()
                            for clazz in clazzs:
                                clazz_json  = clazz.json()
                                del clazz_json['creator']
                                clazz_json['is_creator']=member.is_creator
                                clazzs_json.append(clazz_json)
                        if len(clazzs_json) > 0:
                            student_json = student.json()
                            del student_json['user']
                            student_json['clazzs'] = clazzs_json
                            items.append(student_json)
                response['data']=items
                return response

        @ns.route('/<string:user_id>/students')
        class GetAllStudentByUserResource(Resource):
            def get(self,user_id):
                '''获取用户创建的所有孩子'''
                response['code']=200
                students = Student.objects(user=ObjectId(user_id)).all()
                items = []
                for student in students:
                    item  = student.json()
                    del item['user']
                    items.append(item)
                response['data']=items
                return response