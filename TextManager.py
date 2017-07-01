import json
import bpy
import base64
import sys

class TextManager():

    @staticmethod
    def textToJson(text):
        textInJson = json.loads('{"name": "", "text": ""}')
        textInJson['name'] = text.name
        if text.as_string():
            textInJson['text'] = base64.b64encode(bytearray(text.as_string(), 'utf-8')).decode()
        return textInJson

    @staticmethod
    def jsonToText(jsonText):
        textInJson = json.loads(jsonText)
        textName = textInJson['name']
        textText = base64.b64decode(textInJson['text']).decode("utf-8")
        textObj = None
        if textName in bpy.data.texts and textText == bpy.data.texts[textName].as_string():
            textObj = bpy.data.texts[textName]
        else:
            textObj = bpy.data.texts.new(name = textName)
            textObj.from_string(textText)
            textObj.name = textName
        return textObj

    @staticmethod
    def toBis(text, tags = ''):
        if text.as_string():
            textJson = __class__.textToJson(text)
            request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                'for': 'set_text',
                'text': json.dumps(textJson),
                'text_name': textJson['name'],
                'text_tags': tags
            })
            rez = {"stat": "ERR", "data": {"text": "Error to save"}}
            if request:
                rez = json.loads(request.text)
                if rez['stat'] != 'OK':
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message = rez['data']['text'])
            return rez

    @staticmethod
    def fromBis(id):
        rez = {"stat": "ERR", "data": {"text": "No Id", "content": None}}
        if(id):
            request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                'for': 'get_text',
                'id': id
            })
            if request:
                rez = json.loads(request.text)
        if rez['stat'] != 'OK':
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = rez['data']['text'])
        else:
            __class__.jsonToText(rez['data']['content'])
        return rez
