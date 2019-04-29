# Nikita Akimov
# interplanety@interplanety.org

import bpy
from . import WebRequests
from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class BISNodesPanel(Panel):
    bl_idname = 'BIS_PT_nodes_panel'
    bl_label = 'BIS - MATERIALS'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'BIS'

    def draw(self, context):
        layout = self.layout
        if WebRequests.WebAuthVars.logged:
            if WebRequests.WebAuthVars.userProStatus:
                layout.prop(context.window_manager.bis_get_nodes_info_from_storage_vars, 'searchFilter')
                layout.operator('bis.get_nodes_info_from_storage', icon='VIEWZOOM', text=' Search')
                row = layout.row()
                row.operator('bis.get_nodes_info_from_storage_prev_page', text='Prev')
                row.operator('bis.get_nodes_info_from_storage_next_page', text='Next')
            else:
                layout.operator('bis.get_nodes_info_from_storage', icon='FILE_REFRESH', text=' Get active materials')
            layout.prop(context.window_manager.bis_get_nodes_info_from_storage_vars, 'updatePreviews')
            layout.separator()
            layout.separator()
            layout.template_icon_view(context.window_manager.bis_get_nodes_info_from_storage_vars, 'items', show_labels=True)
            layout.separator()
            layout.separator()
            layout.prop(context.window_manager.bis_add_nodegroup_to_storage_vars, 'tags')
            layout.label(text='(comma separated)')
            button = layout.operator('bis.add_nodegroup_to_storage', text='Save')
            button.show_message = True
            button = layout.operator('bis.update_nodegroup_in_storage', text='Update')
            button.show_message = True
            if context.area.spaces.active.tree_type != 'CompositorNodeTree':
                layout.separator()
                layout.prop(context.preferences.addons[__package__].preferences, 'use_node_group_as', expand=True)
            layout.separator()
            layout.separator()
            layout.operator('dialog.web_auth', icon='FILE_TICK', text='Sign out')
        else:
            layout.operator('dialog.web_auth', icon='WORLD', text='Sign in')


class BISNodesToolsPanel(Panel):
    bl_idname = 'BIS_PT_nodes_tools_panel'
    bl_label = 'Tools'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'BIS'

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text='Add input/output to node group')
        row = box.row()
        row.prop(context.window_manager.bis_nodes_tools_vars, 'io_type', expand=True)
        row = box.row(align=True)
        button = row.operator('bis.add_node_group_io', icon='ADD', text='Input')
        button.in_out = 'IN'
        button = row.operator('bis.add_node_group_io', icon='ADD', text='Output')
        button.in_out = 'OUT'


def register():
    register_class(BISNodesPanel)
    register_class(BISNodesToolsPanel)


def unregister():
    unregister_class(BISNodesToolsPanel)
    unregister_class(BISNodesPanel)
