import bpy
import sys

class BIS_textsPanel(bpy.types.Panel):
    bl_idname = 'bis.texts_panel'
    bl_label = 'BIS'
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        if sys.modules[modulesNames['WebRequests']].WebAuthVars.logged:
            self.layout.operator('dialog.web_auth', icon = 'FILE_TICK', text = 'Sign out')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.scene.bis_add_text_to_storage_vars, 'tags')
            addTextButton = self.layout.operator('bis.add_text_to_storage', icon = 'SCRIPTWIN', text = 'Add text to BIS')
            addTextButton.showMessage = True
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.window_manager.bis_get_texts_info_from_storage_vars, 'searchFilter')
            self.layout.operator('bis.get_texts_info_from_storage', icon = 'SCRIPTWIN', text = 'Search in BIS')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.window_manager.bis_get_texts_info_from_storage_vars, 'items')
        else:
            self.layout.operator('dialog.web_auth', icon = 'WORLD', text = 'Sign in')

def register():
    bpy.utils.register_class(BIS_textsPanel)

def unregister():
    bpy.utils.unregister_class(BIS_textsPanel)
