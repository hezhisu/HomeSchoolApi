import json
from flask import request
from flask_restplus import Resource
import time
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'
class UserLogin(object):
    def __init__(self,api,ns):
        self.api = api
        self.ns = ns


        parser_login = self.api.parser()
        parser_login.add_argument('phone', type=str, required=True, help='手机号', location='query')
        parser_login.add_argument('password', type=str, required=True, help='密码(ASE加密)', location='query')
        @self.ns.route('/session')
        class LoginResource(Resource):

            @self.api.doc(parser=parser_login)
            def get(self):
                '''用户登录'''
                _phone = request.args.get('phone', '')
                _password = request.args.get('password', '')
                response = {'code': 200,'msg': '', 'data': ''}
                user = User.objects(phone = _phone).exclude('password').first()
                if user == None:
                    response['code'] = 201
                    response['msg'] = '手机号未注册'
                else:
                    if  User.objects(phone = _phone).only('password').first().password != _password:
                        response['code'] = 202
                        response['msg'] = '密码错误'
                    else:
                        response['code'] = 200
                        dicdata = json.loads(user.to_json())
                        dicdata['user_id'] = dicdata['_id']['$oid']
                        del dicdata['_id']
                        dicdata['login_time'] = int(time.time()*1000)
                        response['data'] =dicdata
                        response['msg']  = '登录成功'
                return response