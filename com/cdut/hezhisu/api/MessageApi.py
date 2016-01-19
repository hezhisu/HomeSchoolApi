from com.cdut.hezhisu.resource.MessageBiz import MessageBiz

__author__ = 'hezhisu'

##消息相关
class MessageApi(object):
    def __init__(self,api):
        self.api = api
        self.ns = api.namespace('message', description='消息相关')
    def load_resource(self):
        self.biz = MessageBiz(self.api,self.ns)