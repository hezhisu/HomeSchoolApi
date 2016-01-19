from com.cdut.hezhisu.resource.UserBiz import UserBiz
from com.cdut.hezhisu.resource.UserLogin import UserLogin
from com.cdut.hezhisu.resource.UserRegister import UserRegister

__author__ = 'hezhisu'
#用户相关

class UserApi(object):
    def __init__(self,api):
        self.api =api
        self.ns = api.namespace('user', description='用户相关')



    def load_resource(self):
        self.login = UserLogin(self.api,self.ns)
        self.register = UserRegister(self.api,self.ns)
        self.modify = UserBiz(self.api,self.ns)

