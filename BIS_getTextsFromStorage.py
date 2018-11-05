# Nikita Akimov
# interplanety@interplanety.org

import bpy
import json
from . import WebRequests
from . import BIS_Items


class BISGetTextsInfoFromStorage(bpy.types.Operator):
    bl_idname = 'bis.get_texts_info_from_storage'
    bl_label = 'BIS_GetTextsInfoFromBIS'
    bl_description = 'Search texts in BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        request = WebRequests.WebRequest.send_request({
            'for': 'get_items',
            'storage': context.area.spaces.active.type,
            'search_filter': context.window_manager.bis_get_texts_info_from_storage_vars.searchFilter
        })
        if request:
            rez = json.loads(request.text)
            if rez['stat'] == 'OK':
                BIS_Items.BIS_Items.createItemsList(rez['data']['items'], context.area.spaces.active.type, previews=False)
        return {'FINISHED'}


class BISGetTextsInfoFromStorageVars(bpy.types.PropertyGroup):
    searchFilter = bpy.props.StringProperty(
        name='Search',
        description='Filter to search',
        default=''
    )
    items = bpy.props.EnumProperty(
        items=lambda self, context: BIS_Items.BIS_Items.getPreviews(self, context),
        update=lambda self, context: BIS_Items.BIS_Items.onPreviewSelect(self, context)
    )


def register():
    bpy.utils.register_class(BISGetTextsInfoFromStorage)
    bpy.utils.register_class(BISGetTextsInfoFromStorageVars)
    bpy.types.WindowManager.bis_get_texts_info_from_storage_vars = bpy.props.PointerProperty(type=BISGetTextsInfoFromStorageVars)


def unregister():
    del bpy.types.WindowManager.bis_get_texts_info_from_storage_vars
    bpy.utils.unregister_class(BISGetTextsInfoFromStorageVars)
    bpy.utils.unregister_class(BISGetTextsInfoFromStorage)
