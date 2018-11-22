# Nikita Akimov
# interplanety@interplanety.org

import bpy
from .BIS_Items import BIS_Items
from .node_manager import NodeManager


class BISGetNodesInfoFromStorage(bpy.types.Operator):
    bl_idname = 'bis.get_nodes_info_from_storage'
    bl_label = 'BIS: get items'
    bl_description = 'Search nodegroups in BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeManager.items_from_bis(
            context,
            search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.searchFilter,
            page=0,
            update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.updatePreviews
        )
        return {'FINISHED'}


class BISGetNodesInfoFromStoragePrevPage(bpy.types.Operator):
    bl_idname = 'bis.get_nodes_info_from_storage_prev_page'
    bl_label = 'BIS: get items (prev page)'
    bl_description = 'Get prev page'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeManager.items_from_bis(
            context,
            search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.searchFilter,
            page=context.window_manager.bis_get_nodes_info_from_storage_vars.current_page - 1,
            update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.updatePreviews
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bis_get_nodes_info_from_storage_vars.current_page > 0


class BISGetNodesInfoFromStorageNextPage(bpy.types.Operator):
    bl_idname = 'bis.get_nodes_info_from_storage_next_page'
    bl_label = 'BIS: get items (next page)'
    bl_description = 'Get next page'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        NodeManager.items_from_bis(
            context,
            search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.searchFilter,
            page=context.window_manager.bis_get_nodes_info_from_storage_vars.current_page + 1,
            update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.updatePreviews
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bis_get_nodes_info_from_storage_vars.current_page_status not in ('', 'EOF')


class BISGetNodesInfoFromStorageVars(bpy.types.PropertyGroup):
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
    current_page = bpy.props.IntProperty(
        default=0
    )
    current_page_status = bpy.props.StringProperty(
        default=''
    )


def register():
    bpy.utils.register_class(BISGetNodesInfoFromStorage)
    bpy.utils.register_class(BISGetNodesInfoFromStoragePrevPage)
    bpy.utils.register_class(BISGetNodesInfoFromStorageNextPage)
    bpy.utils.register_class(BISGetNodesInfoFromStorageVars)
    bpy.types.WindowManager.bis_get_nodes_info_from_storage_vars = bpy.props.PointerProperty(type=BISGetNodesInfoFromStorageVars)


def unregister():
    del bpy.types.WindowManager.bis_get_nodes_info_from_storage_vars
    bpy.utils.unregister_class(BISGetNodesInfoFromStorageVars)
    bpy.utils.unregister_class(BISGetNodesInfoFromStorageNextPage)
    bpy.utils.unregister_class(BISGetNodesInfoFromStoragePrevPage)
    bpy.utils.unregister_class(BISGetNodesInfoFromStorage)
