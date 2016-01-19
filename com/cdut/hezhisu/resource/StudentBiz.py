import json
from flask import request
from flask_restplus import Resource
from com.cdut.hezhisu.model.Student import Student
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'
class StudentBiz(object):
    def __init__(self,api,ns):

        response = {}
        add_student_parser = api.parser()
        add_student_parser.add_argument('student_name', type=str, required=True, help='学生姓名', location='form')
        add_student_parser.add_argument('identify', type=str, required=True, help='与学生关系', location='form')
        add_student_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='form')

        @ns.route('')
        class AddStudentResource(Resource):
            @api.doc(parser=add_student_parser)
            def post(self):
                '''添加孩子'''
                student = Student()

                user_id = request.form.get('user_id')
                identify = request.form.get('identify')
                student_name = request.form.get('student_name')
                user = User.objects(id=user_id).first()

                student.user = user
                student.identify = identify
                student.student_name = student_name
                student.save()
                response['code']=200
                response['msg']='创建孩子成功'
                response['data']=student.json()
                return response