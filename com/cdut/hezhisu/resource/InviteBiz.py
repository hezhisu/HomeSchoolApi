from flask import request
from flask_restplus import Resource
from com.cdut.hezhisu.main.RedisHelper import RedisOperation
from com.cdut.hezhisu.main.ShortUrl import shorturl

__author__ = 'hezhisu'
class InviteBiz(object):
    def __init__(self,api,ns):

        get_invite_url_parser = api.parser()
        get_invite_url_parser.add_argument('clazz_id', type=str, required=True, help='班级ID', location='query')
        @ns.route('/url')
        class GetInviteUrl(Resource):
            @api.doc(parser=get_invite_url_parser)
            def get(self):
                '''获取邀请链接'''
                host = 'http://127.0.0.1:4000/invite/'
                clazz_id = request.args.get('clazz_id','')
                response = {}
                response['code']=200
                original_url = ''.join([host,clazz_id])
                key = shorturl(original_url)
                RedisOperation().save(key,original_url)
                response['data']= ''.join([host,key])
                return response
        @ns.route('/<string:key>')
        class InviteResource(Resource):
            def get(self,key):
                response = {}
                response['code']=200
                response['data'] = RedisOperation().get(key).decode()
                return response