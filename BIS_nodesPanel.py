# Nikita Akimov
# interplanety@interplanety.org

import bpy
from . import WebRequests


class BIS_nodesPanel(bpy.types.Panel):
    bl_idname = 'bis.nodes_panel'
    bl_label = 'BIS'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'BIS'

    def draw(self, context):
        if WebRequests.WebAuthVars.logged:
            self.layout.operator('dialog.web_auth', icon = 'FILE_TICK', text = 'Sign out')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.scene.bis_add_nodegroup_to_storage_vars, 'tags')
            button = self.layout.operator('bis.add_nodegroup_to_storage', icon='SCRIPTWIN', text='Add nodegroup to BIS')
            button.showMessage = True
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.window_manager.bis_get_nodes_info_from_storage_vars, 'searchFilter')
            self.layout.operator('bis.get_nodes_info_from_storage', icon='SCRIPTWIN', text='Search in BIS')
            self.layout.prop(bpy.context.window_manager.bis_get_nodes_info_from_storage_vars, 'updatePreviews')
            self.layout.separator()
            self.layout.separator()
            self.layout.template_icon_view(bpy.context.window_manager.bis_get_nodes_info_from_storage_vars, 'items')
            self.layout.prop(bpy.context.window_manager.bis_get_nodes_info_from_storage_vars, 'items')
        else:
            self.layout.operator('dialog.web_auth', icon='WORLD', text='Sign in')


def register():
    bpy.utils.register_class(BIS_nodesPanel)


def unregister():
    bpy.utils.unregister_class(BIS_nodesPanel)
