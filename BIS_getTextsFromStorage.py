# Nikita Akimov
# interplanety@interplanety.org

import bpy
import json
from . import WebRequests
from . import BIS_Items


class BIS_getTextsInfoFromStorage(bpy.types.Operator):
    bl_idname = 'bis.get_texts_info_from_storage'
    bl_label = 'BIS_GetTextsInfoFromBIS'
    bl_description = 'Search texts in BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        request = WebRequests.WebRequest.sendRequest({
            'for': 'get_items',
            'storage': context.area.spaces.active.type,
            'search_filter': context.window_manager.bis_get_texts_info_from_storage_vars.searchFilter
        })
        if request:
            searchRez = json.loads(request.text)
            if searchRez['stat'] == 'OK':
                BIS_Items.BIS_Items.createItemsList(searchRez['data']['items'], context.area.spaces.active.type, previews=False)
        return {'FINISHED'}


class BIS_getTextsInfoFromStorageVars(bpy.types.PropertyGroup):
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
    bpy.utils.register_class(BIS_getTextsInfoFromStorage)
    bpy.utils.register_class(BIS_getTextsInfoFromStorageVars)
    bpy.types.WindowManager.bis_get_texts_info_from_storage_vars = bpy.props.PointerProperty(type=BIS_getTextsInfoFromStorageVars)


def unregister():
    del bpy.types.WindowManager.bis_get_texts_info_from_storage_vars
    bpy.utils.unregister_class(BIS_getTextsInfoFromStorageVars)
    bpy.utils.unregister_class(BIS_getTextsInfoFromStorage)
