from flask_restplus import swagger, Api, Resource
from com.cdut.hezhisu.resource.ClazzBiz import ClazzBiz

__author__ = 'hezhisu'
#班级相关

class ClazzApi(object):
    def __init__(self,api):
        self.api = api
        self.ns = api.namespace('clazz', description='班级相关')
    def load_resource(self):
        self.biz = ClazzBiz(self.api,self.ns)
