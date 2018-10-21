# Nikita Akimov
# interplanety@interplanety.org

import json
import bpy
import base64
import sys
from . import WebRequests


class TextManager:

    @staticmethod
    def text_to_json(text):
        text_in_json = json.loads('{"name": "", "text": ""}')
        text_in_json['name'] = text.name
        if text.as_string():
            text_in_json['text'] = base64.b64encode(bytearray(text.as_string(), 'utf-8')).decode()
        return text_in_json

    @staticmethod
    def json_to_text(json_text):
        text_in_json = json.loads(json_text)
        text_name = text_in_json['name']
        text_text = base64.b64decode(text_in_json['text']).decode("utf-8")
        text_obj = None
        if text_name in bpy.data.texts and text_text == bpy.data.texts[text_name].as_string():
            text_obj = bpy.data.texts[text_name]
        else:
            text_obj = bpy.data.texts.new(name=text_name)
            text_obj.from_string(text_text)
            text_obj.name = text_name
        return text_obj

    @staticmethod
    def to_bis(text, tags=''):
        if text.as_string():
            text_in_json = __class__.text_to_json(text)
            tags += (';' if tags else '') + '{0[0]}.{0[1]}'.format(bpy.app.version)
            request = WebRequests.WebRequest.send_request({
                'for': 'add_item',
                'storage': __class__.storage_type(),
                'item_body': json.dumps(text_in_json),
                'item_name': text_in_json['name'],
                'item_tags': tags
            })
            rez = {"stat": "ERR", "data": {"text": "Error to save"}}
            if request:
                rez = json.loads(request.text)
                if rez['stat'] != 'OK':
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['data']['text'])
            return rez

    @staticmethod
    def from_bis(bis_text_id):
        rez = {"stat": "ERR", "data": {"text": "No Id", "content": None}}
        if bis_text_id:
            request = WebRequests.WebRequest.send_request({
                'for': 'get_item',
                'storage': __class__.storage_type(),
                'id': bis_text_id
            })
            if request:
                rez = json.loads(request.text)
        if rez['stat'] != 'OK':
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['data']['text'])
        else:
            __class__.json_to_text(rez['data']['item'])
        return rez

    @staticmethod
    def storage_type():
        # return context.area.spaces.active.type
        return 'TEXT_EDITOR'
