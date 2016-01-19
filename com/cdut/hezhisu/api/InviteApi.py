from com.cdut.hezhisu.resource.InviteBiz import InviteBiz

__author__ = 'hezhisu'
###邀请相关
class InviteApi(object):
    def __init__(self,api):
        self.api = api
        self.ns = api.namespace('invite', description='邀请相关')
    def load_resource(self):
        self.biz = InviteBiz(self.api,self.ns)