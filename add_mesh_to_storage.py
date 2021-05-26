# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

import bpy
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty, BoolProperty, StringProperty
from bpy.types import Operator, PropertyGroup, WindowManager
from .mesh_manager import MeshManager
from . import cfg


class BISAddMeshToStorage(Operator):
    bl_idname = 'bis.add_mesh_to_storage'
    bl_label = 'BIS_AddToIStorage'
    bl_description = 'Add mesh to the BIS'
    bl_options = {'REGISTER'}

    mesh_by_name: StringProperty(
        name='mesh_by_name',
        description='Add mesh by name',
        default=''
    )
    show_message: BoolProperty(
        default=False
    )

    def execute(self, context):
        if self.mesh_by_name:
            objects = [bpy.data.objects[self.mesh_by_name]]
        else:
            objects = context.selected_objects[:]
        if objects:
            request_rez = MeshManager.to_bis(
                context=context,
                objects=objects,
                name=context.window_manager.bis_add_mesh_to_storage_vars.name,
                tags=context.window_manager.bis_add_mesh_to_storage_vars.tags
            )
            if request_rez['stat'] == 'OK':
                context.window_manager.bis_add_mesh_to_storage_vars.name = ''
                context.window_manager.bis_add_mesh_to_storage_vars.tags = ''
                if self.show_message:
                    bpy.ops.bis.messagebox(
                        'INVOKE_DEFAULT',
                        message=request_rez['stat'] + ': ' + request_rez['data']['text']
                    )
            else:
                if cfg.show_debug_err:
                    print(request_rez)
        else:
            bpy.ops.bis.messagebox('INVOKE_DEFAULT', message='No selected Meshes')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.active_object and context.active_object.mode == 'OBJECT'


class BISAddMeshToStorageVars(PropertyGroup):
    name: StringProperty(
        name='Name',
        description='Mesh name',
        default=''
    )
    tags: StringProperty(
        name='Tags (comma separated)',
        description='Add some tags to describe this object',
        default=''
    )


def register():
    register_class(BISAddMeshToStorageVars)
    WindowManager.bis_add_mesh_to_storage_vars = PointerProperty(type=BISAddMeshToStorageVars)
    register_class(BISAddMeshToStorage)


def unregister():
    unregister_class(BISAddMeshToStorage)
    del WindowManager.bis_add_mesh_to_storage_vars
    unregister_class(BISAddMeshToStorageVars)
