import datetime
import json
import threading
from bson import ObjectId
from flask import request
from flask_restplus import Resource
from mongoengine import Q
import time
from com.cdut.hezhisu.main.Push import send_publish_message_push
from com.cdut.hezhisu.model.Attachment import Attachment
from com.cdut.hezhisu.model.Comment import Comment
from com.cdut.hezhisu.model.Member import Member
from com.cdut.hezhisu.model.Message import Message
from com.cdut.hezhisu.model.User import User

__author__ = 'hezhisu'

class MessageBiz(object):
    def __init__(self,api,ns):
        publish_message_parser = api.parser()
        publish_message_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='form')
        publish_message_parser.add_argument('clazz_id', type=str, required=True, help='班级ID', location='form')
        publish_message_parser.add_argument('title', type=str, required=True, help='标题', location='form')
        publish_message_parser.add_argument('content', type=str, required=True, help='内容', location='form')
        publish_message_parser.add_argument('attachments', type=str, required=False, help='附件', location='form')

        @ns.route('')
        @api.doc(description="附件格式为JSON数组 : [{'width':120,'height':120,'key':'dioasndaiodnao21310ns'}]")
        class PublishMessageResource(Resource):
            @api.doc(parser=publish_message_parser)
            def post(self):
                '''发布消息'''
                response = {}
                args = publish_message_parser.parse_args()
                message = Message()
                message.content = args['content']
                message.title = args['title']

                user = User.objects(id=args['user_id']).only('name').first()
                message.publisher = user.name
                message.publisher_id = args['user_id']
                message.clazz_id = args['clazz_id']
                message.create_time = time.time()*1000

                members = Member.objects(Q(clazz_id=args['clazz_id']) & Q(status=1)).only('user')
                unread_users = []
                for member in members:
                    if str(member.user.id) != args['user_id']:
                        unread_users.append(member.user)
                message.unread_users = unread_users
                if args['attachments'] != None:
                    items = eval(args['attachments'])
                    mongo_attachments = []
                    for item in items:
                        attachment = Attachment()
                        attachment.width = item['width']
                        attachment.height = item['height']
                        attachment.url = "http://qiniu1.com/" + item['key']
                        mongo_attachments.append(attachment)
                    message.attachments = mongo_attachments
                message.save()
                response['code']=200
                response['msg']='发送消息成功'
                response['data']=message.json(False)


                threading.Thread(target=send_publish_message_push, args=(unread_users,message.id)).start()
                return response

        get_message_parser = api.parser()
        get_message_parser.add_argument('mode', type=int, required=True, help='-1表示只要消息已看人数和评论人数'\
                                                                               ',0表示只要消息主体,1表示还有要消息详情'
                                        , location='query')
        del_message_parser = api.parser()
        del_message_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='query')

        @ns.route("/<string:message_id>")
        class GetMessageByIdResource(Resource):
            @api.doc(parser=get_message_parser)
            def get(self,message_id):
                '''获取单条消息'''
                response={}
                response['code']=200
                mode = int(request.args.get('mode'))
                if mode==0:
                    message = Message.objects(id=message_id).first()
                    response['data']=message.json(False)
                elif mode==1:
                    message = Message.objects(id=message_id).first()
                    response['data']=message.json(True)
                else:
                    message = Message.objects(id=message_id).only('read_users').only('comments').first()
                    response_data = {}
                    response_data['read_users_count']=len(message.read_users)
                    response_data['comments_count']=len(message.comments)
                    response['data']=response_data
                return response
            @api.doc(parser=del_message_parser)
            def delete(self,message_id):
                '''删除一条消息'''
                response={}
                user_id = request.args.get('user_id')
                message = Message.objects(id=message_id).first()
                if str(message.publisher_id)==user_id:
                    message.delete()
                    response['msg']='删除成功'
                    response['code']=200
                else:
                    response['msg']='只有消息发布者才能删除'
                    response['code']=208;
                return response
        set_message_read_parser = api.parser()
        set_message_read_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='form')
        @ns.route('/<string:message_id>/read')
        class SetMessageReadResource(Resource):
            @api.doc(parser=set_message_read_parser)
            def put(self,message_id):
                '''设置消息已读'''
                args = set_message_read_parser.parse_args()
                message = Message.objects(id=message_id).first()
                if message.publisher_id == args['user_id']:
                    return {'code':200}
                user = User.objects(id=args['user_id']).first()
                if user not in  message.read_users :
                    message.read_users.append(user)
                message.update(set__read_users=message.read_users)
                return {'code':200}


        ###评论
        add_comment_parser = api.parser()
        add_comment_parser.add_argument('user_id', type=str, required=True, help='用户ID', location='form')
        add_comment_parser.add_argument('content', type=str, required=True, help='评论内容', location='form')
        @ns.route('/<string:message_id>/comment')
        class AddCommnetResource(Resource):
            @api.doc(parser=add_comment_parser)
            def put(self,message_id):
                '''发布评论'''
                args = add_comment_parser.parse_args()
                message = Message.objects(id=message_id).first()
                user = User.objects(id=args['user_id']).first()
                comment = Comment()
                comment.comment_id = str(ObjectId.from_datetime(generation_time=datetime.datetime.now()))
                comment.content = args['content']
                comment.publisher = user.name
                comment.publisher_id = str(user.id)
                comment.publish_time = time.time() * 1000
                message.comments.append(comment)
                message.update(comments = message.comments)
                return {'code':200,'msg':'发布评论成功'}
        @ns.route('/<string:message_id>/comment/<string:comment_id>')
        class DelCommentResource(Resource):
            def delete(self,message_id,comment_id):
                '''删除评论'''
                message = Message.objects(id=message_id).first()
                message.comments.remove(message.comments.get(comment_id=comment_id))
                message.comments.save()
                # index = 0
                # for comment in message.comments:
                #     if comment.comment_id == comment_id:
                #         break
                #     index+=1
                # del message.comments[index]
                # message.update(comments=message.comments)
                return {'code':200,'msg':'删除评论成功'}



