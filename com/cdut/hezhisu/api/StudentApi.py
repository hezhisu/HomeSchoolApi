from com.cdut.hezhisu.resource.StudentBiz import StudentBiz

__author__ = 'hezhisu'

class StudentApi(object):
    def __init__(self,api):
        self.api =api
        self.ns = api.namespace('student', description='学生相关')



    def load_resource(self):
        self.biz = StudentBiz(self.api,self.ns)