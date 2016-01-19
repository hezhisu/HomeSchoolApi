import json
from flask import request
from flask_restplus import Resource
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'
class UserRegister(object):
    def __init__(self,api,ns):
        self.api = api
        self.ns = ns
        response ={}
        parser_register = self.api.parser()
        parser_register.add_argument('name', type=str, required=True, help='姓名', location='form')
        parser_register.add_argument('phone', type=str, required=True, help='手机号', location='form')
        parser_register.add_argument('password', type=str, required=True, help='密码(ASE加密)', location='form')

        @self.ns.route('')
        class RegisterResource(Resource):
            @self.api.doc(parser = parser_register)
            def post(self):
                '''用户注册'''
                user = User()
                user.name = request.form['name']
                user.phone = request.form['phone']
                user.password = request.form['password']
                user.save()
                response['code'] = 200
                dicdata = json.loads(user.to_json())
                dicdata['user_id'] = dicdata['_id']['$oid']
                del dicdata['_id']
                response['data'] =dicdata
                response['msg']  = '注册成功'
                return response