# Nikita Akimov
# interplanety@interplanety.org

import json
import sys
import bpy
import base64
from .WebRequests import WebRequest
from .bis_items import BISItems
from .addon import Addon


class TextManager:

    @staticmethod
    def items_from_bis(context, search_filter, page):
        # get page of items list from BIS
        rez = None
        request = WebRequest.send_request(
            context=context,
            data={
                'for': 'get_items',
                'storage': __class__.storage_type(),
                'search_filter': search_filter,
                'page': page,
            }
        )
        if request:
            request_rez = json.loads(request.text)
            rez = request_rez['stat']
            if request_rez['stat'] == 'OK':
                if not request_rez['data']['items']:
                    if getattr(context.window_manager, __package__.lower()+'_web_auth_vars').userProStatus:
                        bpy.ops.message.messagebox('INVOKE_DEFAULT', message='Nothing found')
                    else:
                        bpy.ops.message.messagebox('INVOKE_DEFAULT', message='You do not have any active texts.\n \
                         Please log in your account on the BIS web site,\n \
                         Add some texts to the active palette,\n \
                         And press this button again.')
                BISItems.create_items_list(request_rez['data']['items'], context.area.spaces.active.type, previews=False)
                context.window_manager.bis_get_texts_info_from_storage_vars.current_page = page
                context.window_manager.bis_get_texts_info_from_storage_vars.current_page_status = request_rez['data']['status']
        return rez

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
    def to_bis(context, text, tags=''):
        rez = {"stat": "ERR", "data": {"text": "Error to save"}}
        if text.as_string():
            text_in_json = __class__.text_to_json(text)
            tags += (';' if tags else '') + '{0[0]}.{0[1]}'.format(bpy.app.version)
            request = WebRequest.send_request(
                context=context,
                data={
                    'for': 'add_item',
                    'storage': __class__.storage_type(),
                    'item_body': json.dumps(text_in_json),
                    'item_name': text_in_json['name'],
                    'item_tags': tags,
                    'addon_version': Addon.current_version()
                }
            )
            if request:
                rez = json.loads(request.text)
                if rez['stat'] == 'OK':
                    text['bis_uid'] = rez['data']['id']
                else:
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['data']['text'])
        else:
            rez['data']['text'] = 'Empty Text'
        return rez

    @staticmethod
    def from_bis(context, bis_text_id):
        rez = {"stat": "ERR", "data": {"text": "No Id", "content": None}}
        if bis_text_id:
            request = WebRequest.send_request(
                context=context,
                data={
                    'for': 'get_item',
                    'storage': __class__.storage_type(),
                    'id': bis_text_id
                }
            )
            if request:
                rez = json.loads(request.text)
        if rez['stat'] == 'OK':
            text = __class__.json_to_text(rez['data']['item'])
            if text:
                text['bis_uid'] = bis_text_id
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['data']['text'])
        return rez

    @staticmethod
    def update_in_bis(context, bis_uid, text):
        rez = {"stat": "ERR", "data": {"text": "Error to update"}}
        if text.as_string():
            text_in_json = __class__.text_to_json(text)
            request = WebRequest.send_request(
                context=context,
                data={
                    'for': 'update_item',
                    'storage': __class__.storage_type(),
                    'item_body': json.dumps(text_in_json),
                    'item_name': text_in_json['name'],
                    'item_id': bis_uid
                }
            )
            if request:
                rez = json.loads(request.text)
                if rez['stat'] != 'OK':
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['data']['text'])
        else:
            rez['data']['text'] = 'Empty Text'
        return rez

    @staticmethod
    def storage_type():
        # return context.area.spaces.active.type
        return 'TEXT_EDITOR'
