# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

# node_tree class

from . import cfg
from .file_manager import FileManager
from .node import Node
from .bl_types import BlTypes


class NodeTree:
    @classmethod
    def to_json(cls, node_tree_parent, node_tree):
        node_tree_json = {
            'class': node_tree.__class__.__name__,
            'instance': {
                'type': node_tree.type,
                # 'tree_type': bpy.context.area.spaces.active.tree_type,
                'bl_idname': node_tree.bl_idname,
                'name': node_tree.name,
                'inputs': [],
                'outputs': [],
                'nodes': [],
                'links': []
            }
        }
        cls._enumerate(node_tree)
        # node_tree inputs
        for c_input in node_tree.inputs:
            input_json = BlTypes.to_json(
                instance=c_input
            )
            input_json['bl_socket_idname'] = c_input.bl_socket_idname
            node_tree_json['instance']['inputs'].append(input_json)
        # node_tree outputs
        for c_output in node_tree.outputs:
            output_json = BlTypes.to_json(
                instance=c_output
            )
            output_json['bl_socket_idname'] = c_output.bl_socket_idname
            node_tree_json['instance']['outputs'].append(output_json)
        # node tree nodes
        # process first - because they influence on other nodes and must be created first
        preordered_nodes = [node for node in node_tree.nodes if node.type in ['FRAME']]
        # all other nodes
        nodes = [node for node in node_tree.nodes if node not in preordered_nodes]
        # first - preordered nodes, next - all other nodes
        all_nodes = preordered_nodes + nodes
        for node in all_nodes:
            node_json = Node.to_json(
                node=node
            )
            node_tree_json['instance']['nodes'].append(node_json)
        # links
        for link in node_tree.links:
            from_node = link.from_node['bis_node_uid']
            to_node = link.to_node['bis_node_uid']
            # for group nodes, reroute and group inputs/output nodes - by number, for other nodes - by identifier
            if link.from_node.type in ['GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT', 'REROUTE']:
                from_output = link.from_node.outputs[:].index(link.from_socket)
            else:
                from_output = link.from_socket.identifier
            if link.to_node.type in ['GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT', 'REROUTE']:
                to_input = link.to_node.inputs[:].index(link.to_socket)
            else:
                to_input = link.to_socket.identifier
            node_tree_json['instance']['links'].append([from_node, from_output, to_node, to_input])
        return node_tree_json

    @classmethod
    def from_json(cls, node_tree_parent, node_tree_json, attachments_path, bis_version=None):
        if node_tree_parent and node_tree_json:
            node_tree = node_tree_parent.node_tree
            # node_tree inputs/outputs
            # node_tree inputs - now do nothing
            # for input_number, input_json in enumerate(node_tree_json['inputs']):
            #     # for NodeSocketInterfaceXXX - do nothing
            #     # for NodeSocketXXX - work in node_node_group
            #     pass
            # # node outputs
            # for output_number, output_json in enumerate(node_tree_json['outputs']):
            #     # for NodeSocketInterfaceXXX - do nothing
            #     # for NodeSocketXXX - work in node_node_group
            #     pass
            # node_tree inputs
            for input_number, input_json in enumerate(node_tree_json['instance']['inputs']):
                # NodeSocketInterfaceXXX
                # name can be empty
                input_name = input_json['instance']['name'] if 'name' in input_json['instance'] else ''
                new_input = node_tree.inputs.new(
                    type=input_json['bl_socket_idname'],
                    name=input_name
                )
                BlTypes.complex_from_json(
                    instance=new_input,
                    json=input_json,
                    excluded_attributes=['bl_idname', 'name', 'type']
                )
            # node outputs
            for output_number, output_json in enumerate(node_tree_json['instance']['outputs']):
                # NodeSocketInterfaceXXX
                # name can be empty
                output_name = output_json['instance']['name'] if 'name' in output_json['instance'] else ''
                new_output = node_tree.outputs.new(
                    type=output_json['bl_socket_idname'],
                    name=output_name
                )
                BlTypes.complex_from_json(
                    instance=new_output,
                    json=output_json,
                    excluded_attributes=['bl_idname', 'name', 'type']
                )
            # Nodes
            for current_node_in_json in node_tree_json['instance']['nodes']:
                # Nodes
                node = None
                try:
                    # current node type may not exists - if node saved from future version of Blender
                    node = node_tree.nodes.new(type=current_node_in_json['class'])
                except Exception as exception:
                    if cfg.show_debug_err:
                        print(repr(exception))
                if node:
                    Node.from_json(
                        node=node,
                        node_json=current_node_in_json,
                        attachments_path=attachments_path
                    )
                    # frames (NodeFrame nodes must be processed in first order, before all other nodes)
                    if 'parent' in current_node_in_json['instance']:
                        parent_node = cls._node_by_bis_id(
                            node_tree=node_tree,
                            bis_node_id=current_node_in_json['instance']['parent']['instance']['bis_node_uid']
                        )
                        node.parent = parent_node
                        node.location += parent_node.location
            # links
            for link_json in node_tree_json['instance']['links']:
                from_node = cls._node_by_bis_id(node_tree=node_tree, bis_node_id=link_json[0])
                to_node = cls._node_by_bis_id(node_tree=node_tree, bis_node_id=link_json[2])
                if from_node and to_node:
                    # for group nodes and group inputs/output nodes - by number, for other nodes - by identifier
                    if isinstance(link_json[1], str):
                        from_output = cls._output_by_identifier(from_node, link_json[1])
                    else:
                        from_output = from_node.outputs[link_json[1]]
                    if isinstance(link_json[3], str):
                        to_input = cls._input_by_identifier(to_node, link_json[3])
                    else:
                        to_input = to_node.inputs[link_json[3]]
                    if from_output and to_input:
                        node_tree.links.new(from_output, to_input)

    @staticmethod
    def clear(node_tree, exclude_output_nodes=False):
        # clear node_tree except Output node
        for node in node_tree.nodes:
            if not (exclude_output_nodes and node.bl_idname in ['ShaderNodeOutputMaterial', 'CompositorNodeComposite', 'ShaderNodeOutputWorld']):
                node_tree.nodes.remove(node)

    @staticmethod
    def has_node_groups(node_tree):
        # return True if node_tree has NodeGroup nodes
        return any(node.type == 'GROUP' for node in node_tree.nodes)

    @staticmethod
    def _enumerate(node_tree, start=0):
        # enumerates all nodes in node_tree
        for node in node_tree.nodes:
            start += 1
            node['bis_node_uid'] = start
        return start

    @staticmethod
    def _node_by_bis_id(node_tree, bis_node_id):
        rez = None
        for node in node_tree.nodes:
            if 'bis_node_uid' in node and node['bis_node_uid'] == bis_node_id:
                rez = node
        return rez

    @classmethod
    def _input_by_identifier(cls, node, identifier):
        # returns input by its identifier
        rez = None
        if identifier:
            input_with_identifier = [node_input for node_input in node.inputs[:]
                                     if node_input.identifier == identifier]
            if input_with_identifier:
                rez = input_with_identifier[0]
        return rez

    @classmethod
    def _output_by_identifier(cls, node, identifier):
        # returns output by its identifier
        rez = None
        if identifier:
            output_with_identifier = [node_output for node_output in node.outputs[:]
                                      if node_output.identifier == identifier]
            if output_with_identifier:
                rez = output_with_identifier[0]
        return rez

    @classmethod
    def external_items(cls, node_tree):
        # returns external items (textures,... etc) list
        rez = []
        for node in node_tree.nodes:
            if node.type == 'GROUP':
                rez.extend(cls.external_items(node_tree=node.node_tree))
            elif node.type == 'TEX_IMAGE' and node.image:
                rez.append({
                    'path': FileManager.abs_path(node.image.filepath),
                    'name': node.image.name
                })
            elif node.type == 'SCRIPT' and node.mode == 'EXTERNAL' and node.filepath:
                rez.append({
                    'path': FileManager.abs_path(node.filepath)
                })
        return rez
