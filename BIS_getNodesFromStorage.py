# Nikita Akimov
# interplanety@interplanety.org

import bpy
import json
from .WebRequests import WebRequest
from .BIS_Items import BIS_Items
from .NodeManager import NodeManager


class BIS_getNodesInfoFromStorage(bpy.types.Operator):
    bl_idname = 'bis.get_nodes_info_from_storage'
    bl_label = 'BIS_AddToIStorage'
    bl_description = 'Search nodegroups in BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        request = WebRequest.sendRequest({
            'for': 'search_nodes',
            'search_filter': context.window_manager.bis_get_nodes_info_from_storage_vars.searchFilter,
            'subtype': NodeManager.get_subtype(context),
            'subtype2': NodeManager.get_subtype2(context),
            'update_preview': context.window_manager.bis_get_nodes_info_from_storage_vars.updatePreviews
        })
        if request:
            searchRez = json.loads(request.text)
            if searchRez['stat'] == 'OK':
                previewToUpdate = BIS_Items.updatePreviewsFromData(searchRez['data']['items'], context.area.spaces.active.type)
                if previewToUpdate:
                    request = WebRequest.sendRequest({
                        'for': 'update_previews',
                        'preview_list': previewToUpdate,
                        'storage_type': context.area.spaces.active.type
                    })
                    if request:
                        previewsUpdateRez = json.loads(request.text)
                        if previewsUpdateRez['stat'] == 'OK':
                            BIS_Items.updatePreviewsFromData(previewsUpdateRez['data']['items'], context.area.spaces.active.type)
                BIS_Items.createItemsList(searchRez['data']['items'], context.area.spaces.active.type)
        return {'FINISHED'}


class BIS_getNodesInfoFromStorageVars(bpy.types.PropertyGroup):
    searchFilter = bpy.props.StringProperty(
        name='Search',
        description='Filter to search',
        default=''
    )
    updatePreviews = bpy.props.BoolProperty(
        name='Update Previews',
        description='Update previews from server',
        default=False
    )
    items = bpy.props.EnumProperty(
        items=lambda self, context: BIS_Items.getPreviews(self, context),
        update=lambda self, context: BIS_Items.onPreviewSelect(self, context)
    )


def register():
    bpy.utils.register_class(BIS_getNodesInfoFromStorage)
    bpy.utils.register_class(BIS_getNodesInfoFromStorageVars)
    bpy.types.WindowManager.bis_get_nodes_info_from_storage_vars = bpy.props.PointerProperty(type = BIS_getNodesInfoFromStorageVars)


def unregister():
    del bpy.types.WindowManager.bis_get_nodes_info_from_storage_vars
    bpy.utils.unregister_class(BIS_getNodesInfoFromStorageVars)
    bpy.utils.unregister_class(BIS_getNodesInfoFromStorage)
