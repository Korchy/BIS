# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


from bpy.types import Operator, PropertyGroup, WindowManager
from bpy.props import PointerProperty, StringProperty, BoolProperty, IntProperty, EnumProperty
from bpy.utils import register_class, unregister_class
from .bis_items import BISItems
from .node_manager import NodeManager
from .geometry_nodes_manager import GeometryNodesManager


class BISGetNodesInfoFromStorage(Operator):
    bl_idname = 'bis.get_nodes_info_from_storage'
    bl_label = 'BIS: get items'
    bl_description = 'Search node groups in BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.preferences.addons[__package__].preferences.default_mode_in_3d_view == 'GN':
            GeometryNodesManager.items_from_bis(
                context=context,
                search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.search_filter,
                page=0,
                update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.update_previews
            )
        else:
            NodeManager.items_from_bis(
                context=context,
                search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.search_filter,
                page=0,
                update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.update_previews
            )
        return {'FINISHED'}


class BISGetNodesInfoFromStoragePrevPage(Operator):
    bl_idname = 'bis.get_nodes_info_from_storage_prev_page'
    bl_label = 'BIS: get items (prev page)'
    bl_description = 'Get prev page'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.preferences.addons[__package__].preferences.default_mode_in_3d_view == 'GN':
            GeometryNodesManager.items_from_bis(
                context=context,
                search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.search_filter,
                page=context.window_manager.bis_get_nodes_info_from_storage_vars.current_page - 1,
                update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.update_previews
            )
        else:
            NodeManager.items_from_bis(
                context=context,
                search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.search_filter,
                page=context.window_manager.bis_get_nodes_info_from_storage_vars.current_page - 1,
                update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.update_previews
            )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bis_get_nodes_info_from_storage_vars.current_page > 0


class BISGetNodesInfoFromStorageNextPage(Operator):
    bl_idname = 'bis.get_nodes_info_from_storage_next_page'
    bl_label = 'BIS: get items (next page)'
    bl_description = 'Get next page'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.preferences.addons[__package__].preferences.default_mode_in_3d_view == 'GN':
            GeometryNodesManager.items_from_bis(
                context=context,
                search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.search_filter,
                page=context.window_manager.bis_get_nodes_info_from_storage_vars.current_page + 1,
                update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.update_previews
            )
        else:
            NodeManager.items_from_bis(
                context=context,
                search_filter=context.window_manager.bis_get_nodes_info_from_storage_vars.search_filter,
                page=context.window_manager.bis_get_nodes_info_from_storage_vars.current_page + 1,
                update_preview=context.window_manager.bis_get_nodes_info_from_storage_vars.update_previews
            )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bis_get_nodes_info_from_storage_vars.current_page_status not in ('', 'EOF')


class BISGetNodesInfoFromStorageVars(PropertyGroup):
    search_filter: StringProperty(
        name='Search',
        description='Filter to search',
        default=''
    )
    update_previews: BoolProperty(
        name='Update Previews',
        description='Update previews from server',
        default=False
    )
    items: EnumProperty(
        items=lambda self, context: BISItems.get_previews(NodeManager.storage_type(context)),
        update=lambda self, context: BISItems.on_preview_select(self, NodeManager.storage_type(context))
    )
    current_page: IntProperty(
        default=0
    )
    current_page_status: StringProperty(
        default=''
    )


def register():
    register_class(BISGetNodesInfoFromStorage)
    register_class(BISGetNodesInfoFromStoragePrevPage)
    register_class(BISGetNodesInfoFromStorageNextPage)
    register_class(BISGetNodesInfoFromStorageVars)
    WindowManager.bis_get_nodes_info_from_storage_vars = PointerProperty(
        type=BISGetNodesInfoFromStorageVars
    )


def unregister():
    del WindowManager.bis_get_nodes_info_from_storage_vars
    unregister_class(BISGetNodesInfoFromStorageVars)
    unregister_class(BISGetNodesInfoFromStorageNextPage)
    unregister_class(BISGetNodesInfoFromStoragePrevPage)
    unregister_class(BISGetNodesInfoFromStorage)
