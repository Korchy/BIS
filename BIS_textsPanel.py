import bpy
import sys

class BIS_textsPanel(bpy.types.Panel):
    bl_idname = 'bis.texts_panel'
    bl_label = 'BIS'
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        if sys.modules[modulesNames['WebRequests']].WebAuthVars.logged:
            self.layout.operator('dialog.web_auth', icon = 'FILE_TICK', text = 'Logged')
            self.layout.separator()
            self.layout.separator()
        else:
            self.layout.operator('dialog.web_auth', icon = 'WORLD', text = 'Please login')

def register():
    bpy.utils.register_class(BIS_textsPanel)

def unregister():
    bpy.utils.unregister_class(BIS_textsPanel)
