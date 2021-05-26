# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


import bpy
from bpy.props import BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .TextManager import TextManager


class BISUpdateText(Operator):
    bl_idname = 'bis.update_text_in_storage'
    bl_label = 'Update Text'
    bl_description = 'Update text in the BIS'
    bl_options = {'REGISTER', 'UNDO'}

    show_message: BoolProperty(
        default=False
    )

    def execute(self, context):
        current_text = context.area.spaces.active.text
        if 'bis_uid' in current_text:
            rez = TextManager.update_in_bis(context=context, bis_uid=current_text['bis_uid'], text=current_text)
            if rez['stat'] == 'OK':
                if self.show_message:
                    bpy.ops.bis.messagebox('INVOKE_DEFAULT', message=rez['stat'] + ': ' + rez['data']['text'])
            else:
                bpy.ops.bis.messagebox('INVOKE_DEFAULT', message=rez['stat'] + ': ' + rez['data']['text'])
        else:
            bpy.ops.bis.messagebox('INVOKE_DEFAULT', message='ERR: First save this Text to the BIS!')
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.label(text='Update current Text in the BIS storage?')
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


def register():
    register_class(BISUpdateText)


def unregister():
    unregister_class(BISUpdateText)
