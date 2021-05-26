# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


import bpy
from bpy.props import BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from .mesh_manager import MeshManager
from . import cfg


class BISUpdateMeshInStorage(Operator):
    bl_idname = 'bis.update_mesh_in_storage'
    bl_label = 'Update mesh'
    bl_description = 'Update mesh in the BIS'
    bl_options = {'REGISTER', 'UNDO'}

    show_message: BoolProperty(
        default=False
    )

    def execute(self, context):
        # update
        request_rez = MeshManager.update_in_bis(
            context=context,
            objects=context.selected_objects,
            bis_uid=MeshManager.get_bis_uid(context=context),
        )
        if request_rez['stat'] != 'OK':
            if cfg.show_debug_err:
                print(request_rez['stat'] + ': ' + request_rez['data']['text'])
        if self.show_message:
            bpy.ops.bis.messagebox(
                'INVOKE_DEFAULT',
                message=request_rez['stat'] + ': ' + request_rez['data']['text']
            )
        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.separator()
        layout.label(text='Update selected Meshes in the BIS?')
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    @classmethod
    def poll(cls, context):
        return bool(MeshManager.get_bis_uid(context=context))


def register():
    register_class(BISUpdateMeshInStorage)


def unregister():
    unregister_class(BISUpdateMeshInStorage)
