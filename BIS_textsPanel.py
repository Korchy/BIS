# Nikita Akimov
# interplanety@interplanety.org

import bpy
from . import WebRequests


class BIS_textsPanel(bpy.types.Panel):
    bl_idname = 'bis.texts_panel'
    bl_label = 'BIS'
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'

    def draw(self, context):
        if WebRequests.WebAuthVars.logged:
            self.layout.operator('dialog.web_auth', icon='FILE_TICK', text='Sign out')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.scene.bis_add_text_to_storage_vars, 'tags')
            button = self.layout.operator('bis.add_text_to_storage', text=' Add')
            button.showMessage = True
            button = self.layout.operator('bis.update_text_in_storage', text=' Update')
            button.showMessage = True
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.window_manager.bis_get_texts_info_from_storage_vars, 'searchFilter')
            self.layout.operator('bis.get_texts_info_from_storage', icon='VIEWZOOM', text='Search')
            self.layout.separator()
            self.layout.separator()
            self.layout.prop(bpy.context.window_manager.bis_get_texts_info_from_storage_vars, 'items')
        else:
            self.layout.operator('dialog.web_auth', icon='WORLD', text='Sign in')


def register():
    bpy.utils.register_class(BIS_textsPanel)


def unregister():
    bpy.utils.unregister_class(BIS_textsPanel)
