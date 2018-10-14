# Nikita Akimov
# interplanety@interplanety.org

import sys
import bpy
import os
import json
from . import cfg
from .NodeNodeGroup import *


class NodeManager:
    @staticmethod
    def node_group_to_json(nodegroup):
        # convert node group to json
        group_in_json = None
        if nodegroup.type == 'GROUP':
            __class__.enumerate_nodes(nodegroup)
            nodegroup_class = 'Node' + nodegroup.bl_idname
            if hasattr(sys.modules[__name__], nodegroup_class):
                group_in_json = getattr(sys.modules[__name__], nodegroup_class).node_to_json(nodegroup)
                if cfg.to_server_to_file:
                    with open(os.path.join(os.path.dirname(bpy.data.filepath), 'send_to_server.json'), 'w') as currentFile:
                        json.dump(group_in_json, currentFile, indent=4)
                if cfg.no_sending_to_server:
                    return None
        return group_in_json

    @staticmethod
    def json_to_node_group(dest_nodetree, node_in_json):
        # recreate node group from json
        if cfg.from_server_to_file:
            with open(os.path.join(os.path.dirname(bpy.data.filepath), 'received_from_server.json'), 'w') as currentFile:
                json.dump(node_in_json, currentFile, indent=4)
        current_node = None
        if dest_nodetree:
            if hasattr(sys.modules[__name__], 'Node' + node_in_json['bl_type']):
                node_class = getattr(sys.modules[__name__], 'Node' + node_in_json['bl_type'])
                current_node = node_class.json_to_node(node_tree=dest_nodetree, node_in_json=node_in_json)
                current_node.location = (0, 0)
        return current_node

    @staticmethod
    def get_subtype(context):
        # return subtype
        return context.area.spaces.active.tree_type

    @staticmethod
    def get_subtype2(context):
        # return subtype2
        return context.area.spaces.active.shader_type

    @staticmethod
    def is_procedural(material):
        # check if material (nodegroup) is fully procedural - has no one texture nodes
        rez = True
        for node in material.node_tree.nodes:
            if node.type == 'GROUP':
                rez = __class__.is_procedural(node)
                if not rez:
                    break
            elif node.type == 'TEX_IMAGE':
                rez = False
                break
        return rez

    @staticmethod
    def enumerate_nodes(material, start=-1):
        # enumerates all nodes in node_tree and all nodes in all its subtrees
        node_id = start + 1
        material['BIS_node_id'] = node_id
        for node in material.node_tree.nodes:
            node_id += 1
            node['BIS_node_id'] = node_id
            if node.type == 'GROUP':
                node_id = __class__.enumerate_nodes(node, node_id)
        return node_id
