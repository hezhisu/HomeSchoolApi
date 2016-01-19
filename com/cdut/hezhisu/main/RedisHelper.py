from flask.json import JSONEncoder
import redis
__author__ = 'hezhisu'

class RedisOperation(object):
    def __init__(self):
        self.redis = redis.StrictRedis(host='localhost',port=6379,db=0)
        self.push_json={}

    def set_channel(self,channel):
        self.channel= channel

    def set_push_type(self,type):
        self.push_json['type']=type

    def set_push_ids(self,push_ids):
        self.push_json['push_ids']=push_ids

    def set_push_content(self,content):
        self.push_json['data']=content

    def push(self):
        self.redis.publish(self.channel,JSONEncoder().encode(self.push_json))

    def save(self,key,value):
        self.redis.set(key,value)

    def get(self,key):
        return self.redis.get(key)




