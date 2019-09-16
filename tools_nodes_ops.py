# Nikita Akimov
# interplanety@interplanety.org

import bpy
from bpy.types import Operator, PropertyGroup, WindowManager
from bpy.props import PointerProperty, StringProperty
from bpy.utils import register_class, unregister_class
from .node_manager import NodeManager
from .tools_nodes import NodesTools


class BIS_OT_tools_nodes_add_node_group_io(Operator):
    bl_idname = 'bis.tools_nodes_add_node_group_io'
    bl_label = 'Add input/output'
    bl_description = 'Add input/output to active node group'
    bl_options = {'REGISTER', 'UNDO'}

    in_out: StringProperty(
        name='IN_OUT',
        default='IN'
    )

    def execute(self, context):
        active_node = NodeManager.active_node(context=context)
        if self.in_out == 'IN':
            NodesTools.add_input_to_node(node=active_node,
                                         input_type=context.window_manager.bis_tools_nodes_vars.io_type,
                                         input_name='input')
        elif self.in_out == 'OUT':
            NodesTools.add_output_to_node(node=active_node,
                                          output_type=context.window_manager.bis_tools_nodes_vars.io_type,
                                          output_name='output')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        active_node = NodeManager.active_node(context=context)
        if active_node and active_node.select and active_node.type == 'GROUP':
            return True
        return False


class BISNodesToolsVars(PropertyGroup):
    io_type: bpy.props.EnumProperty(
        items=[
            ('NodeSocketInt', 'Int', 'Int', '', 0),
            ('NodeSocketFloat', 'Float', 'Float', '', 1),
            ('NodeSocketColor', 'Color', 'Color', '', 2),
            ('NodeSocketVector', 'Vector', 'Vector', '', 3),
            ('NodeSocketShader', 'BSDF', 'Shader', '', 4)
        ],
        default='NodeSocketInt'
    )


def register():
    register_class(BIS_OT_tools_nodes_add_node_group_io)
    register_class(BISNodesToolsVars)
    WindowManager.bis_tools_nodes_vars = PointerProperty(type=BISNodesToolsVars)


def unregister():
    del WindowManager.bis_tools_nodes_vars
    unregister_class(BISNodesToolsVars)
    unregister_class(BIS_OT_tools_nodes_add_node_group_io)
