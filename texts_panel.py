# Nikita Akimov
# interplanety@interplanety.org

from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from . import WebRequests


class BISTextsPanel(Panel):
    bl_idname = 'bis.texts_panel'
    bl_label = 'BIS - TEXTS'
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'BIS'

    def draw(self, context):
        layout = self.layout
        if WebRequests.WebAuthVars.logged:
            if WebRequests.WebAuthVars.userProStatus:
                layout.prop(context.window_manager.bis_get_texts_info_from_storage_vars, 'search_filter')
                layout.operator('bis.get_texts_info_from_storage', icon='VIEWZOOM', text=' Search')
                row = layout.row()
                row.operator('bis.get_texts_info_from_storage_prev_page', text='Prev')
                row.operator('bis.get_texts_info_from_storage_next_page', text='Next')
            else:
                layout.operator('bis.get_texts_info_from_storage', icon='FILE_REFRESH', text=' Get active palette')
            layout.separator()
            layout.separator()
            layout.prop(context.window_manager.bis_get_texts_info_from_storage_vars, 'items')
            layout.separator()
            layout.separator()
            layout.prop(context.window_manager.bis_add_text_to_storage_vars, 'tags')
            layout.label(text='(comma separated)')
            button = layout.operator('bis.add_text_to_storage', text='Save')
            button.show_message = True
            button = layout.operator('bis.update_text_in_storage', text='Update')
            button.show_message = True
            layout.separator()
            layout.separator()
            layout.operator('dialog.web_auth', icon='FILE_TICK', text='Sign out')
        else:
            layout.operator('dialog.web_auth', icon='WORLD', text='Sign in')


def register():
    register_class(BISTextsPanel)


def unregister():
    unregister_class(BISTextsPanel)
