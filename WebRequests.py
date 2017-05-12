import bpy
import json
import os
import requests

class WebAuthVars(bpy.types.PropertyGroup):
    logged = bpy.props.BoolProperty(
        name = 'Logged',
        description = 'Is user logged',
        default = False
    )
    host = bpy.props.StringProperty(
        name = 'Host',
        description = 'Host',
        default = ''
    )
    userLoginSaved = bpy.props.StringProperty(
        name = 'User Login Saved',
        description = 'Saved user login',
        default = ''
    )
    token = bpy.props.StringProperty(
        name = 'Token',
        description = 'Token',
        default = ''
    )
    requestBase = bpy.props.StringProperty(
        name = 'Request Base',
        description = 'Request base',
        default = ''
    )

class WebAuth(bpy.types.Operator):
    bl_idname = "dialog.web_auth"
    bl_label = "Authorization"

    userLogin = bpy.props.StringProperty(
        name = "Login",
        description = "User Login",
        default = ''
    )
    userPassword = bpy.props.StringProperty(
        subtype = 'PASSWORD',
        name = "Password",
        description = "User Password",
        default = ''
    )
    WebAuthVars.logged = False
    WebAuthVars.host = ''
    WebAuthVars.userLoginSaved = ''
    WebAuthVars.token = ''
    WebAuthVars.requestBase = ''

    def execute(self, context):
        self.logIn()
        for area in bpy.context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}

    def invoke(self, context, event):
        self.logOff()
        if WebAuthVars.userLoginSaved != '':
            self.userLogin = WebAuthVars.userLoginSaved
        return context.window_manager.invoke_props_dialog(self)

    @classmethod
    def getInitData(cls):
        with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.json') as currentFile:
            jsonData = json.load(currentFile)
            WebAuthVars.host = jsonData['host']
            WebAuthVars.requestBase = jsonData['requestbase']
            if 'userLogin' in jsonData:
                WebAuthVars.userLoginSaved = jsonData['userLogin']

    def logIn(self):
        session = WebRequestsVars.getSession()
        data = {'requestbase': WebAuthVars.requestBase, 'userlogin': self.userLogin, 'userpassword': self.userPassword}
        self.userPassword = ''
        request = session.post(WebAuthVars.host+'/blender_auth', data = data)
        requestRez = json.loads(request.text)
        if requestRez['stat'] == 'T':
            WebAuthVars.logged = True
            WebAuthVars.token = requestRez['token']
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = requestRez['txt'])
            self.logOff()

    def logOff(self):
        WebAuthVars.token = ''
        WebAuthVars.logged = False
        WebRequestsVars.closeSession()

class WebRequestsVars():
    session = None

    @staticmethod
    def getSession():
        if not WebRequestsVars.session:
            WebRequestsVars.session = requests.Session()
        return WebRequestsVars.session

    @staticmethod
    def closeSession():
        if WebRequestsVars.session:
            WebRequestsVars.session.close()
            WebRequestsVars.session = None

class WebRequest():
    @staticmethod
    def sendRequest(data = {}):
        requestData = {'requestbase': WebAuthVars.requestBase, 'token': WebAuthVars.token}
        requestData.update(data)
        request = WebRequestsVars.session.post(WebAuthVars.host+'/blender_request', data = requestData)
        return request

def register():
    bpy.utils.register_class(WebAuthVars)
    bpy.utils.register_class(WebAuth)
    WebAuth.getInitData()

def unregister():
    bpy.utils.unregister_class(WebAuth)
    bpy.utils.unregister_class(WebAuthVars)

if __name__ == "__main__":
    register()
