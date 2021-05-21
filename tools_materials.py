# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

class ToolsMaterials:

    @staticmethod
    def material_from_active_object_to_selected(context):
        # copy material from active object to all selected objects
        active_object = context.active_object
        if active_object:
            material = context.active_object.active_material
            selected_objects = context.selected_objects[:]
            if active_object in selected_objects:
                selected_objects.remove(active_object)
            for obj in selected_objects:
                obj.active_material = material
