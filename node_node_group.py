# Nikita Akimov
# interplanety@interplanety.org

import bpy
import sys
from .addon import Addon
from .node_tree import NodeTree
from .NodeNodeGroup import *    # 1.4.1
from .node_common import NodeCommon
from .node_shader_cycles import *
from .node_compositor import *


class NodeGroup:

    @classmethod
    def to_json(cls, nodegroup):
        group_in_json = None
        if nodegroup.type == 'GROUP':
            nodegroup_class = 'Node' + nodegroup.bl_idname
            if hasattr(sys.modules[__name__], nodegroup_class):
                group_in_json = getattr(sys.modules[__name__], nodegroup_class).node_to_json(nodegroup)
        return group_in_json

    @classmethod
    def from_json(cls, node_group_json, parent_node_tree, attachments_path):
        node_group = None
        if parent_node_tree:
            # for older compatibility (v 1.4.1)
            # if all node groups becomes 1.4.2. and later - remove all "else" condition
            node_group_version = node_group_json['BIS_addon_version'] if 'BIS_addon_version' in node_group_json else Addon.node_group_first_version
            if Addon.node_group_version_higher(node_group_version, Addon.node_group_first_version):
                # 1.4.2 and later
                node_class = getattr(sys.modules[__name__], 'Node' + node_group_json['bl_idname'])
            else:
                # 1.4.1
                node_class = getattr(sys.modules[__name__], 'NodeBase' + node_group_json['bl_type'])
            node_group = node_class.json_to_node(node_tree=parent_node_tree, node_json=node_group_json, attachments_path=attachments_path)
            node_group.location = (0, 0)
        return node_group


class NodeShaderNodeGroup(NodeCommon):

    @classmethod
    def node_to_json(cls, node):
        # enumerate nodes in group
        cls.enumerate(node)
        return super().node_to_json(node)

    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        node_json['tree_type'] = bpy.context.area.spaces.active.tree_type
        node_json['name'] = node.node_tree.name
        node_json['node_tree'] = NodeTree.to_json(node_tree_parent=node, node_tree=node.node_tree)
        node_json['BIS_addon_version'] = Addon.current_version()
        return node_json

    @classmethod
    def _json_to_node_spec(cls, node, node_json, attachments_path):
        node['BIS_addon_version'] = node_json['BIS_addon_version'] if 'BIS_addon_version' in node_json else Addon.node_group_first_version
        if Addon.node_group_version_equal_or_less(node['BIS_addon_version'], '1.7.0'):
            # for 1.7.0 and less - nodes and links are separate
            # this can be removed if there would no v. 1.7.0 and less materials/nodegroups in the BIS lbrary
            # Nodes
            for current_node_in_json in node_json['nodes']:
                node_class = NodeCommon
                if hasattr(sys.modules[__name__], 'Node' + current_node_in_json['bl_idname']):
                    node_class = getattr(sys.modules[__name__], 'Node' + current_node_in_json['bl_idname'])
                node_class.json_to_node(node_tree=node.node_tree, node_json=current_node_in_json, attachments_path=attachments_path)
            # links
            for link_json in node_json['links']:
                from_node = cls._node_by_bis_id(node.node_tree, link_json[0])
                to_node = cls._node_by_bis_id(node.node_tree, link_json[2])
                if from_node and to_node:
                    # for group nodes and group inputs/output nodes - by number, for other nodes - by identifier
                    if isinstance(link_json[1], str):
                        from_output = cls.output_by_identifier(from_node, link_json[1])
                    else:
                        from_output = from_node.outputs[link_json[1]]
                    if isinstance(link_json[3], str):
                        to_input = cls.input_by_identifier(to_node, link_json[3])
                    else:
                        to_input = to_node.inputs[link_json[3]]
                    if from_output and to_input:
                        node.node_tree.links.new(from_output, to_input)
            # Frames
            for c_node in node.node_tree.nodes:
                if c_node['parent_str']:
                    parent_node = node.node_tree.nodes[c_node['parent_str']]
                    c_node.parent = parent_node
                    c_node.location += parent_node.location
        else:
            # v. 1.7.1 and higher - nodes and links in node_tree
            NodeTree.from_json(node_tree_parent=node, node_tree_json=node_json['node_tree'], attachments_path=attachments_path)

    @staticmethod
    def enumerate(node, start=0):
        # enumerates all nodes in the group
        # don't enumerate node group itself - not to loose if it is already enumerated by parent node group
        for current_node in node.node_tree.nodes:
            start += 1
            current_node['BIS_node_id'] = start
        return start

    @staticmethod
    def _node_by_bis_id(node_tree, bis_node_id):
        rez = None
        for node in node_tree.nodes:
            if 'BIS_node_id' in node and node['BIS_node_id'] == bis_node_id:
                rez = node
        return rez


class NodeCompositorNodeGroup(NodeShaderNodeGroup):
    pass
