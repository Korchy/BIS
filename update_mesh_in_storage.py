# Nikita Akimov
# interplanety@interplanety.org

import bpy
from bpy.props import BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
import json
from .node_manager import NodeManager
from .WebRequests import WebRequest
from .addon import Addon


class BISUpdateMeshInStorage(Operator):
    bl_idname = 'bis.update_mesh_in_storage'
    bl_label = 'Update mesh'
    bl_description = 'Update mesh in the BIS'
    bl_options = {'REGISTER', 'UNDO'}

    show_message = BoolProperty(
        default=False
    )

    def execute(self, context):
        print('add mesh to storage ', context.active_object)


        if context.active_object:
            pass
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message='No Mesh selected')
        return {'FINISHED'}

    def draw(self, context):
        self.layout.separator()
        self.layout.label('Update selected Mesh in the BIS?')
        self.layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.mode == 'OBJECT'


def register():
    register_class(BISUpdateMeshInStorage)


def unregister():
    unregister_class(BISUpdateMeshInStorage)
