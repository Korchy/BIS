# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

import bpy
from bpy.props import BoolProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
from . import cfg
from .geometry_nodes_manager import GeometryNodesManager
from .material import Material
from .node_manager import NodeManager


class BISUpdateNodegroup(Operator):
    bl_idname = 'bis.update_nodegroup_in_storage'
    bl_label = 'Update nodegroup'
    bl_description = 'Update nodegroup in the BIS'
    bl_options = {'REGISTER', 'UNDO'}

    show_message: BoolProperty(
        default=True
    )

    def execute(self, context):
        request_rez = {"stat": "ERR", "data": {"text": "Undefined item to update"}}
        item_to_update = None
        subtype = Material.get_subtype(context=context)
        if context.preferences.addons[__package__].preferences.use_node_group_as == 'NODEGROUP' or \
                subtype == 'CompositorNodeTree':
            active_node = NodeManager.active_node(context=context)
            if active_node and active_node.type == 'GROUP':
                item_to_update = active_node  # save active node group
            else:
                request_rez['data']['text'] = 'No selected Node Group'
        elif context.preferences.addons[__package__].preferences.use_node_group_as == 'MATERIAL':
            active_material = NodeManager.active_material(context=context)
            if active_material:
                item_to_update = active_material  # save active material
            else:
                request_rez['data']['text'] = 'No material to save'
        if item_to_update:
            if subtype == 'GeometryNodeTree':
                # geometry nodes
                request_rez = GeometryNodesManager.update_in_bis(
                    context=context,
                    node_tree_container=item_to_update
                )
            else:
                # shader/compositing nodes
                request_rez = NodeManager.update_in_bis(
                    context=context,
                    item=item_to_update,
                    item_type=context.preferences.addons[__package__].preferences.use_node_group_as
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
        layout.label(text='Update current node tree item in the BIS?')
        layout.separator()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)


def register():
    register_class(BISUpdateNodegroup)


def unregister():
    unregister_class(BISUpdateNodegroup)
