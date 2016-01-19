from flask import Flask
from flask_restplus import Api
from com.cdut.hezhisu.api.ClazzApi import ClazzApi
from com.cdut.hezhisu.api.InviteApi import InviteApi
from com.cdut.hezhisu.api.MessageApi import MessageApi
from com.cdut.hezhisu.api.StudentApi import StudentApi
from com.cdut.hezhisu.api.UserApi import UserApi

__author__ = 'hezhisu'
app = Flask(__name__)
api = Api(app, version='1.0', title='HomeSchool API',
                        description='家校通')

userApi = UserApi(api)
userApi.load_resource()

clazzApi = ClazzApi(api)
clazzApi.load_resource()

studentApi = StudentApi(api)
studentApi.load_resource()

messageApi = MessageApi(api)
messageApi.load_resource()

inviteApi = InviteApi(api)
inviteApi.load_resource()

if __name__ == '__main__':
    app.run(debug=True,port=4000,host='0.0.0.0')