import bpy
import sys
import json

class BIS_getNodesInfoFromStorage(bpy.types.Operator):
    bl_idname = 'bis.get_nodes_info_from_storage'
    bl_label = 'BIS_AddToIStorage'
    bl_description = 'Search nodegroups in BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
            'for': 'search_nodes',
            'search_filter': bpy.context.window_manager.bis_get_nodes_info_from_storage_vars.searchFilter,
            'update_preview': bpy.context.window_manager.bis_get_nodes_info_from_storage_vars.updatePreviews
        })
        searchRez = json.loads(request.text)
        if searchRez['stat'] == 'OK':
            previewToUpdate = sys.modules[modulesNames['BIS_Items']].BIS_Items.updatePreviewsFromData(searchRez['data']['items'], context.area.spaces.active.type)
            if previewToUpdate:
                request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                    'for': 'update_previews',
                    'preview_list': previewToUpdate,
                    'storage_type': context.area.spaces.active.type
                })
                previewsUpdateRez = json.loads(request.text)
                if previewsUpdateRez['stat'] == 'OK':
                    sys.modules[modulesNames['BIS_Items']].BIS_Items.updatePreviewsFromData(previewsUpdateRez['data']['items'], context.area.spaces.active.type)
            sys.modules[modulesNames['BIS_Items']].BIS_Items.createItemsList(searchRez['data']['items'], context.area.spaces.active.type)
        return {'FINISHED'}

class BIS_getNodesInfoFromStorageVars(bpy.types.PropertyGroup):
    searchFilter = bpy.props.StringProperty(
        name = 'Search',
        description = 'Filter to search',
        default = ''
    )
    updatePreviews = bpy.props.BoolProperty(
        name = 'Update Previews',
        description = 'Update previews from server',
        default = False
    )
    items = bpy.props.EnumProperty(
        items = lambda self, context: sys.modules[modulesNames['BIS_Items']].BIS_Items.getPreviews(self, context) if 'modulesNames' in globals() else [],
        update = lambda self, context: sys.modules[modulesNames['BIS_Items']].BIS_Items.onPreviewSelect(self, context) if 'modulesNames' in globals() else None
    )

def register():
    bpy.utils.register_class(BIS_getNodesInfoFromStorage)
    bpy.utils.register_class(BIS_getNodesInfoFromStorageVars)
    bpy.types.WindowManager.bis_get_nodes_info_from_storage_vars = bpy.props.PointerProperty(type = BIS_getNodesInfoFromStorageVars)

def unregister():
    del bpy.types.WindowManager.bis_get_nodes_info_from_storage_vars
    bpy.utils.unregister_class(BIS_getNodesInfoFromStorageVars)
    bpy.utils.unregister_class(BIS_getNodesInfoFromStorage)
