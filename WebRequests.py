import bpy
import json
import os
import requests

class WebAuthVars(bpy.types.PropertyGroup):
    logged = bpy.props.BoolProperty(
        default = False
    )
    host = bpy.props.StringProperty(
        default = ''
    )
    userLogin = bpy.props.StringProperty(
        default = ''
    )
    userStayLogged = bpy.props.BoolProperty(
        default = False
    )
    token = bpy.props.StringProperty(
        default = ''
    )
    requestBase = bpy.props.StringProperty(
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
    userStayLogged = bpy.props.BoolProperty(
        name = 'Stay logged (insecure)',
        description = 'Stay logged',
        default = False
    )

    def execute(self, context):
        if WebAuthVars.logged:
            self.logOff()
        else:
            self.logIn()
        for area in bpy.context.screen.areas:
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
    def getInitData(cls):
        WebAuthVars.logged = False
        WebAuthVars.userStayLogged = False
        with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.json') as currentFile:
            jsonData = json.load(currentFile)
            WebAuthVars.host = jsonData['host']
            WebAuthVars.requestBase = jsonData['requestbase']
            if 'userLogin' in jsonData:
                WebAuthVars.userLogin = jsonData['userLogin']
            else:
                WebAuthVars.userLogin = ''
            if 'token' in jsonData:
                WebAuthVars.token = jsonData['token']
            else:
                WebAuthVars.token = ''
            currentFile.close()
        if WebAuthVars.token:
            cls.logIn(cls)

    def logIn(self):
        if WebAuthVars.token:
            WebAuthVars.logged = True
        else:
            session = WebRequestsVars.getSession()
            data = {'requestbase': WebAuthVars.requestBase, 'userlogin': self.userLogin, 'userpassword': self.userPassword}
            self.userPassword = ''
            request = session.post(WebAuthVars.host+'/blender_auth', data = data)
            requestRez = json.loads(request.text)
            if requestRez['stat'] == 'T':
                WebAuthVars.logged = True
                WebAuthVars.token = requestRez['token']
                WebAuthVars.userLogin = self.userLogin
                self.saveConfig(userLogin = WebAuthVars.userLogin,
                                token = WebAuthVars.token if self.userStayLogged else '')
            else:
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message = requestRez['txt'])
                self.logOff()

    def logOff(self):
        WebAuthVars.token = ''
        WebAuthVars.logged = False
        WebRequestsVars.closeSession()
        self.saveConfig(userLogin = WebAuthVars.userLogin)

    def saveConfig(self, userLogin = '', token = ''):
        with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + 'config.json', 'r+') as configFile:
            jsonData = json.load(configFile)
            jsonData['token'] = token
            jsonData['userLogin'] = userLogin
            configFile.seek(0)
            configFile.truncate()
            json.dump(jsonData, configFile, indent = 4)
            configFile.close()

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
        session = WebRequestsVars.getSession()
        request = session.post(WebAuthVars.host+'/blender_request', data = requestData)
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
