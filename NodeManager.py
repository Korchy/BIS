# Nikita Akimov
# interplanety@interplanety.org

import sys
import bpy
import os
import json
from . import cfg
from .NodeNodeGroup import *
from .WebRequests import WebRequest
from .BIS_Items import BIS_Items


class NodeManager:

    @staticmethod
    def items_from_bis(context, search_filter, page, update_preview):
        # get page of items list from BIS
        rez = None
        request = WebRequest.send_request({
            'for': 'get_items',
            'search_filter': search_filter,
            'page': page,
            'storage': __class__.storage_type(context),
            'storage_subtype': __class__.get_subtype(context),
            'storage_subtype2': __class__.get_subtype2(context),
            'update_preview': update_preview
        })
        if request:
            request_rez = json.loads(request.text)
            rez = request_rez['stat']
            if request_rez['stat'] == 'OK':
                preview_to_update = BIS_Items.updatePreviewsFromData(request_rez['data']['items'], __class__.storage_type(context))
                if preview_to_update:
                    request = WebRequest.send_request({
                        'for': 'update_previews',
                        'preview_list': preview_to_update,
                        'storage': __class__.storage_type(context),
                        'storage_subtype': __class__.get_subtype(context),
                        'storage_subtype2': __class__.get_subtype2(context)
                    })
                    if request:
                        previews_update_rez = json.loads(request.text)
                        if previews_update_rez['stat'] == 'OK':
                            BIS_Items.updatePreviewsFromData(previews_update_rez['data']['items'], __class__.storage_type(context))
                BIS_Items.createItemsList(request_rez['data']['items'], __class__.storage_type(context))
                context.window_manager.bis_get_nodes_info_from_storage_vars.current_page = page
                context.window_manager.bis_get_nodes_info_from_storage_vars.current_page_status = request_rez['data']['status']
        return rez

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
        # check if material (nodegroup) is fully procedural
        rez = True
        for node in material.node_tree.nodes:
            if node.type == 'GROUP':
                rez = __class__.is_procedural(node)
                if not rez:
                    break
            elif node.type == 'TEX_IMAGE':
                rez = False
                break
            elif node.type == 'SCRIPT' and node.mode == 'EXTERNAL':
                rez = False
                break
        return rez

    @staticmethod
    def cpu_render_required(material):
        # check if material (nodegroup) required only CPU render
        rez = False
        for node in material.node_tree.nodes:
            if node.type == 'GROUP':
                rez = __class__.cpu_render_required(node)
                if rez:
                    break
            elif node.type == 'SCRIPT':
                rez = True
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

    @staticmethod
    def get_bis_linked_items(key, nodegroup_in_json):
        for k, v in nodegroup_in_json.items():
            if k == key:
                yield v
            elif isinstance(v, dict):
                for result in __class__.get_bis_linked_items(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    if isinstance(d, dict):
                        for result in __class__.get_bis_linked_items(key, d):
                            yield result

    @staticmethod
    def storage_type(context):
        # return context.area.spaces.active.type
        return 'NODE_EDITOR'
