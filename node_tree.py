# Nikita Akimov
# interplanety@interplanety.org

# node_tree class
import sys
from .node_io import *
from .node_common import NodeCommon


class NodeTree:
    @classmethod
    def to_json(cls, node_tree):
        node_tree_json = {
            'type': node_tree.type,
            'bl_idname': node_tree.bl_idname,
            'inputs': [],
            'outputs': [],
            'nodes': [],
            'links': []
        }
        # nodes
        __class__._enumerate(node_tree)
        # node_tree inputs
        for c_input in node_tree.inputs:
            input_name = 'NodeIO' + c_input.bl_idname
            io_class = NodeIOCommon
            if hasattr(sys.modules[__name__], input_name):
                io_class = getattr(sys.modules[__name__], input_name)
            node_tree_json['inputs'].append(io_class.input_to_json(c_input))
        # node_tree outputs
        for c_output in node_tree.outputs:
            output_name = 'NodeIO' + c_output.bl_idname
            io_class = NodeIOCommon
            if hasattr(sys.modules[__name__], output_name):
                io_class = getattr(sys.modules[__name__], output_name)
            node_tree_json['outputs'].append(io_class.output_to_json(c_output))
        # nodes
        for node in node_tree.nodes:
            node_class = NodeCommon
            if hasattr(sys.modules[__name__], 'Node' + node.bl_idname):
                node_class = getattr(sys.modules[__name__], 'Node' + node.bl_idname)
            node_json = node_class.node_to_json(node)
            node_tree_json['nodes'].append(node_json)
        # links
        for link in node_tree.links:
            from_node = link.from_node['BIS_node_id']
            to_node = link.to_node['BIS_node_id']
            # for group nodes, reroute and group inputs/output nodes - by number, for other nodes - by identifier
            if link.from_node.type in ['GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT', 'REROUTE']:
                from_output = link.from_node.outputs[:].index(link.from_socket)
            else:
                from_output = link.from_socket.identifier
            if link.to_node.type in ['GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT', 'REROUTE']:
                to_input = link.to_node.inputs[:].index(link.to_socket)
            else:
                to_input = link.to_socket.identifier
            node_tree_json['links'].append([from_node, from_output, to_node, to_input])
        return node_tree_json

    @classmethod
    def from_json(cls, node_tree_parent, node_tree_json):
        if node_tree_parent and node_tree_json:
            node_tree = node_tree_parent.node_tree
            # node_tree inputs
            for input_number, input_json in enumerate(node_tree_json['inputs']):
                if node_tree_parent.bl_rna.name == 'Group':
                    # for group - generate new input
                    node_tree.inputs.new(type=input_json['bl_idname'], name=input_json['name'])     # NodeSocketInterfaceXXX
                    current_input = node_tree_parent.inputs[-1]   # NodeSocketXXX
                    io_class = NodeIOCommon
                    if hasattr(sys.modules[__name__], 'NodeIO' + input_json['bl_idname']):
                        io_class = getattr(sys.modules[__name__], 'NodeIO' + input_json['bl_idname'])
                    io_class.json_to_i(node_input=current_input, input_json=input_json)
            # node outputs
            for output_number, output_json in enumerate(node_tree_json['outputs']):
                if node_tree_parent.bl_rna.name == 'Group':
                    # for group - generate new output
                    node_tree.outputs.new(type=output_json['bl_idname'], name=output_json['name'])     # NodeSocketInterfaceXXX
                    current_output = node_tree_parent.outputs[-1]   # NodeSocketXXX
                    io_class = NodeIOCommon
                    if hasattr(sys.modules[__name__], 'NodeIO' + output_json['bl_idname']):
                        io_class = getattr(sys.modules[__name__], 'NodeIO' + output_json['bl_idname'])
                    io_class.json_to_o(node_output=current_output, output_json=output_json)
            # Nodes
            for current_node_in_json in node_tree_json['nodes']:
                node_class = NodeCommon
                if hasattr(sys.modules[__name__], 'Node' + current_node_in_json['bl_idname']):
                    node_class = getattr(sys.modules[__name__], 'Node' + current_node_in_json['bl_idname'])
                node_class.json_to_node(node_tree=node_tree, node_json=current_node_in_json)
            # links
            for link_json in node_tree_json['links']:
                from_node = __class__._node_by_bis_id(node_tree=node_tree, bis_node_id=link_json[0])
                to_node = __class__._node_by_bis_id(node_tree=node_tree, bis_node_id=link_json[2])
                # for group nodes and group inputs/output nodes - by number, for other nodes - by identifier
                if isinstance(link_json[1], str):
                    from_output = __class__._output_by_identifier(from_node, link_json[1])
                else:
                    from_output = from_node.outputs[link_json[1]]
                if isinstance(link_json[3], str):
                    to_input = __class__._input_by_identifier(to_node, link_json[3])
                else:
                    to_input = to_node.inputs[link_json[3]]
                if from_output and to_input:
                    node_tree.links.new(from_output, to_input)
            # Frames
            for c_node in node_tree.nodes:
                if c_node['parent_str']:
                    parent_node = node_tree.nodes[c_node['parent_str']]
                    c_node.parent = parent_node
                    c_node.location += parent_node.location

    @staticmethod
    def clear(node_tree):
        # clear node_tree except Output node
        for node in node_tree.nodes:
            if node.bl_idname not in ['ShaderNodeOutputMaterial', 'CompositorNodeComposite']:
                node_tree.nodes.remove(node)

    @staticmethod
    def _enumerate(node_tree, start=0):
        # enumerates all nodes in node_tree
        for node in node_tree.nodes:
            start += 1
            node['BIS_node_id'] = start
        return start

    @staticmethod
    def _node_by_bis_id(node_tree, bis_node_id):
        rez = None
        for node in node_tree.nodes:
            if 'BIS_node_id' in node and node['BIS_node_id'] == bis_node_id:
                rez = node
        return rez

    @classmethod
    def _input_by_identifier(cls, node, identifier):
        # returns input by its identifier
        rez = None
        if identifier:
            input_with_identifier = [node_input for node_input in node.inputs[:] if node_input.identifier == identifier]
            if input_with_identifier:
                rez = input_with_identifier[0]
        return rez

    @classmethod
    def _output_by_identifier(cls, node, identifier):
        # returns output by its identifier
        rez = None
        if identifier:
            output_with_identifier = [node_output for node_output in node.outputs[:] if node_output.identifier == identifier]
            if output_with_identifier:
                rez = output_with_identifier[0]
        return rez
