# Nikita Akimov
# interplanety@interplanety.org

import bpy
from .TextManager import TextManager
from bpy.props import PointerProperty, StringProperty, BoolProperty
from bpy.types import Operator, PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class


class AddTextToStorage(Operator):
    bl_idname = 'bis.add_text_to_storage'
    bl_label = 'AddTextToStorage'
    bl_description = 'Add text to BIS'
    bl_options = {'REGISTER', 'UNDO'}

    text_name: StringProperty(
        name='textName',
        description='Add text with current name',
        default=''
    )
    show_message: BoolProperty(
        default=False
    )

    def execute(self, context):
        if self.text_name:
            current_text = bpy.data.texts[self.text_name]
        else:
            current_text = context.area.spaces.active.text
        rez = TextManager.to_bis(context=context, text=current_text, tags=context.window_manager.bis_add_text_to_storage_vars.tags)
        if rez['stat'] == 'OK':
            context.window_manager.bis_add_text_to_storage_vars.tags = ''
            if self.show_message:
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['data']['text'])
        return {'FINISHED'}


class AddTextToStorageVars(PropertyGroup):
    tags: StringProperty(
        name='Tags (comma separated)',
        description='Add some tags to describe this text',
        default=''
    )


def register():
    register_class(AddTextToStorage)
    register_class(AddTextToStorageVars)
    WindowManager.bis_add_text_to_storage_vars = PointerProperty(type=AddTextToStorageVars)


def unregister():
    del WindowManager.bis_add_text_to_storage_vars
    unregister_class(AddTextToStorageVars)
    unregister_class(AddTextToStorage)
