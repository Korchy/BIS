# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .tools_materials import ToolsMaterials

class BIS_OT_tools_materials_active_to_selected(Operator):
    bl_idname = 'bis.materials_active_to_selected'
    bl_label = 'Material: Active to Selected'
    bl_description = 'Copy material from active object to selected objects'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ToolsMaterials.material_from_active_object_to_selected(context=context)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        selected_objects = context.selected_objects[:]
        if context.active_object in selected_objects:
            selected_objects.remove(context.active_object)
        if context.active_object and selected_objects:
            return True
        return False


def register():
    register_class(BIS_OT_tools_materials_active_to_selected)


def unregister():
    unregister_class(BIS_OT_tools_materials_active_to_selected)
