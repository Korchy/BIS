import bpy
import sys

class BIS_mainPanel(bpy.types.Panel):
    bl_idname = 'bis.panel'
    bl_label = 'Blender Interplanety Store'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = 'Interplanety Store'

    def draw(self, context):
        if sys.modules[modulesNames['WebRequests']].WebAuthVars.logged:
            self.layout.operator('dialog.web_auth', icon = 'FILE_TICK', text = 'Logged')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.scene.bis_add_node_to_store_vars, 'tags')
            self.layout.operator('bis.add_node_to_store', icon = 'SCRIPTWIN', text = 'Add nodegroup to BIS')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.window_manager.bis_get_nodes_info_from_store_vars, 'searchFilter')
            self.layout.operator('bis.get_nodes_info_from_store', icon = 'SCRIPTWIN', text = 'Search in BIS')
            self.layout.prop(bpy.context.window_manager.bis_get_nodes_info_from_store_vars, 'updatePreviews')
            self.layout.separator()
            self.layout.separator()
            self.layout.template_icon_view(bpy.context.window_manager.bis_get_nodes_info_from_store_vars, 'previews')
            self.layout.prop(bpy.context.window_manager.bis_get_nodes_info_from_store_vars, 'previews')
        else:
            self.layout.operator('dialog.web_auth', icon = 'WORLD', text = 'Please login')

def register():
    bpy.utils.register_class(BIS_mainPanel)

def unregister():
    bpy.utils.unregister_class(BIS_mainPanel)
