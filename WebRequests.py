# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
import json
import os
import requests
import platform


class WebAuthVars:
    
    logged = False
    host = ''
    userLogin = ''
    userStayLogged = False
    userProStatus = False
    token = ''
    requestBase = ''


class WebAuth(Operator):
    bl_idname = 'bis.web_auth'
    bl_label = 'Authorization'

    userLogin: StringProperty(
        name='Login',
        description='User Login',
        default=''
    )
    userPassword: StringProperty(
        subtype='PASSWORD',
        name='Password',
        description='User Password',
        default=''
    )
    userStayLogged: BoolProperty(
        name='Stay logged (insecure)',
        description='Stay logged',
        default=False
    )

    def execute(self, context):
        if WebAuthVars.logged:
            __class__.log_off(context=context)
        else:
            self.log_in(context=context)
        for area in context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        if WebAuthVars.logged:
            return self.execute(context)
        else:
            if WebAuthVars.userLogin:
                self.userLogin = WebAuthVars.userLogin
            return context.window_manager.invoke_props_dialog(self)

    @classmethod
    def get_init_data(cls, context):
        WebAuthVars.logged = False
        WebAuthVars.userStayLogged = False
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')) as currentFile:
            json_data = json.load(currentFile)
            WebAuthVars.host = json_data['host']
            WebAuthVars.requestBase = json_data['requestbase']
            if 'userLogin' in json_data:
                WebAuthVars.userLogin = json_data['userLogin']
            else:
                WebAuthVars.userLogin = ''
            if 'token' in json_data:
                WebAuthVars.token = json_data['token']
            else:
                WebAuthVars.token = ''
            currentFile.close()
        if WebAuthVars.token:
            cls.log_in(cls, context=context)

    def log_in(self, context):
        if WebAuthVars.token:
            if __class__.check_token_valid(
                    context=context,
                    user_login=WebAuthVars.userLogin,
                    token=WebAuthVars.token
            ):
                WebAuthVars.logged = True
            else:
                __class__.log_off(context=context)
        else:
            request = WebRequest.send_request(context=context, data={'userlogin': self.userLogin, 'userpassword': self.userPassword}, host_target='blender_auth')
            self.userPassword = ''
            if request:
                request_rez = json.loads(request.text)
                if request_rez['stat'] == 'OK':
                    WebAuthVars.logged = True
                    WebAuthVars.token = request_rez['data']['token']
                    WebAuthVars.userLogin = self.userLogin
                    WebAuthVars.userProStatus = request_rez['data']['prostatus']
                    __class__.save_config(user_login=WebAuthVars.userLogin,
                                          token=WebAuthVars.token if self.userStayLogged else '')
                else:
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=request_rez['data']['text'])
                    __class__.log_off(context=context)

    @staticmethod
    def log_off(context):
        WebAuthVars.token = ''
        WebAuthVars.logged = False
        WebRequestsVars.close_session()
        __class__.save_config(user_login=WebAuthVars.userLogin)

    @staticmethod
    def check_token_valid(context, user_login='', token=''):
        request = WebRequest.send_request(context=context, data={'userlogin': user_login, 'token': token}, host_target='blender_auth')
        if request:
            request_rez = json.loads(request.text)
            if request_rez['stat'] == 'OK':
                WebAuthVars.userProStatus = request_rez['data']['prostatus']
                return True
        return False

    @staticmethod
    def save_config(user_login='', token=''):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json'), 'r+') as configFile:
            json_data = json.load(configFile)
            json_data['token'] = token
            json_data['userLogin'] = user_login
            configFile.seek(0)
            configFile.truncate()
            json.dump(json_data, configFile, indent=4)
            configFile.close()


class WebRequestsVars:
    session = None

    @staticmethod
    def get_session():
        if not WebRequestsVars.session:
            WebRequestsVars.session = requests.Session()
            WebRequestsVars.session.headers.update(
                {
                    'User-Agent': requests.utils.default_headers()['User-Agent'] + ' (' + platform.platform() + ')'
                }
            )
        return WebRequestsVars.session

    @staticmethod
    def close_session():
        if WebRequestsVars.session:
            WebRequestsVars.session.close()
            WebRequestsVars.session = None


class WebRequest:
    @staticmethod
    def send_request(context, data=None, files=None, host_target='blender_request'):
        data = data if data else {}
        files = files if files else {}
        session = WebRequestsVars.get_session()
        request_data = {
            'requestbase': WebAuthVars.requestBase,
            'token': WebAuthVars.token
        }
        request_data.update(data)
        request = None
        try:
            request = session.post(WebAuthVars.host + '/' + host_target, data=request_data, files=files)
        except requests.exceptions.RequestException as error:
            print('ERR: problems with connection to BIS ', error)
        if request:
            if 'text/html' in request.headers['Content-Type']:
                request_rez = None
                try:
                    request_rez = json.loads(request.text)
                except ValueError as error:
                    print(request.text, error)
                    request = None
                if request_rez:
                    if request_rez['stat'] != 'OK':
                        print(request_rez['stat'] + ': ' + (request_rez['data']['text'] if 'data' in request_rez else ''))
        return request


def register():
    register_class(WebAuth)
    WebAuth.get_init_data(context=bpy.context)


def unregister():
    unregister_class(WebAuth)
    WebRequestsVars.close_session()


if __name__ == '__main__':
    register()
