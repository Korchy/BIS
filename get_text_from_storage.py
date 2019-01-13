# Nikita Akimov
# interplanety@interplanety.org

import bpy
from bpy.props import IntProperty, BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .TextManager import TextManager


class GetTextFromStorage(Operator):
    bl_idname = 'bis.get_text_from_storage'
    bl_label = 'BIS_GetFromStorage'
    bl_description = 'Get text from BIS'
    bl_options = {'REGISTER', 'UNDO'}

    text_id: IntProperty(
        name='text_id',
        default=0
    )
    show_message: BoolProperty(
        default=False
    )

    def execute(self, context):
        rez = TextManager.from_bis(self.text_id)
        if rez['stat'] == 'OK':
            if self.show_message:
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['data']['text'])
        return {'FINISHED'}


def register():
    register_class(GetTextFromStorage)


def unregister():
    unregister_class(GetTextFromStorage)
