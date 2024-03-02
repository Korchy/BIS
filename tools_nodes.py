# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

import bpy


class NodesTools:

    @staticmethod
    def add_input_to_node(node, input_type, input_name):
        # add input to node
        if node and node.node_tree:
            if bpy.app.version < (4, 0, 0):
                node.node_tree.inputs.new(input_type, input_name)
            else:
                node.node_tree.interface.new_socket(
                    name=input_name,
                    in_out='INPUT',
                    socket_type=input_type
                )

    @staticmethod
    def add_output_to_node(node, output_type, output_name):
        # add output to node
        if node and node.node_tree:
            if bpy.app.version < (4, 0, 0):
                node.node_tree.outputs.new(output_type, output_name)
            else:
                node.node_tree.interface.new_socket(
                    name=output_name,
                    in_out='OUTPUT',
                    socket_type=output_type
                )
