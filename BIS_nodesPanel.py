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
            self.layout.operator('dialog.web_auth', icon='FILE_TICK', text='Sign out')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(context.scene.bis_add_nodegroup_to_storage_vars, 'tags')
            button = self.layout.operator('bis.add_nodegroup_to_storage', text='Save')
            button.showMessage = True
            button = self.layout.operator('bis.update_nodegroup_in_storage', text='Update')
            button.showMessage = True
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(context.window_manager.bis_get_nodes_info_from_storage_vars, 'searchFilter')
            self.layout.operator('bis.get_nodes_info_from_storage', icon='VIEWZOOM', text=' Search')
            self.layout.prop(context.window_manager.bis_get_nodes_info_from_storage_vars, 'updatePreviews')
            self.layout.separator()
            self.layout.separator()
            self.layout.template_icon_view(context.window_manager.bis_get_nodes_info_from_storage_vars, 'items', show_labels=True)
        else:
            self.layout.operator('dialog.web_auth', icon='WORLD', text='Sign in')


def register():
    bpy.utils.register_class(BIS_nodesPanel)


def unregister():
    bpy.utils.unregister_class(BIS_nodesPanel)
