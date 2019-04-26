# Nikita Akimov
# interplanety@interplanety.org

import sys
import bpy
import os
import json
from . import cfg
from .NodeNodeGroup import *
from .node_node_group import *
from .material import Material
from .addon import Addon
from .WebRequests import WebRequest, WebAuthVars
from .bis_items import BISItems


class NodeManager:

    @staticmethod
    def items_from_bis(context, search_filter, page, update_preview=False):
        # get page of items list from BIS
        rez = None
        storage_subtype = __class__.get_subtype(context)
        storage_subtype2 = __class__.get_subtype2(context)
        request = WebRequest.send_request({
            'for': 'get_items',
            'search_filter': search_filter,
            'page': page,
            'storage': __class__.storage_type(context),
            'storage_subtype': storage_subtype,
            'storage_subtype2': storage_subtype2,
            'update_preview': update_preview
        })
        if request:
            request_rez = json.loads(request.text)
            rez = request_rez['stat']
            if request_rez['stat'] == 'OK':
                if not request_rez['data']['items']:
                    if WebAuthVars.userProStatus:
                        bpy.ops.message.messagebox('INVOKE_DEFAULT', message='Nothing found')
                    else:
                        bpy.ops.message.messagebox('INVOKE_DEFAULT', message='You do not have any active materials.\n \
                         Please log in your account on the BIS web site,\n \
                         Add some materials to the active palette,\n \
                         And press this button again.')
                preview_to_update = BISItems.update_previews_from_data(data=request_rez['data']['items'], list_name=__class__.storage_type(context))
                if preview_to_update:
                    request = WebRequest.send_request({
                        'for': 'update_previews',
                        'preview_list': preview_to_update,
                        'storage': __class__.storage_type(context),
                        'storage_subtype': storage_subtype,
                        'storage_subtype2': storage_subtype2
                    })
                    if request:
                        previews_update_rez = json.loads(request.text)
                        if previews_update_rez['stat'] == 'OK':
                            BISItems.update_previews_from_data(data=previews_update_rez['data']['items'], list_name=__class__.storage_type(context))
                BISItems.create_items_list(data=request_rez['data']['items'], list_name=__class__.storage_type(context))
                context.window_manager.bis_get_nodes_info_from_storage_vars.current_page = page
                context.window_manager.bis_get_nodes_info_from_storage_vars.current_page_status = request_rez['data']['status']
        return rez

    @staticmethod
    def from_bis(context, bis_item_id, item_type):
        # item_type = 'MATERIAL' or 'NODEGROUP'
        request_rez = {"stat": "ERR", "data": {"text": "No Id", "content": None}}
        if bis_item_id:
            subtype = __class__.get_subtype(context)
            request = WebRequest.send_request({
                'for': 'get_item',
                'storage': __class__.storage_type(context=context),
                'storage_subtype': subtype,
                'storage_subtype2': __class__.get_subtype2(context),
                'id': bis_item_id,
                'addon_version': Addon.current_version()
            })
            if request:
                request_rez = json.loads(request.text)
                if request_rez['stat'] == 'OK':
                    node_in_json = json.loads(request_rez['data']['item'])
                    if subtype == 'CompositorNodeTree' and not context.window.scene.use_nodes:
                        context.window.scene.use_nodes = True
                    if item_type == 'MATERIAL':
                        active_node_tree = __class__.active_node_tree(context=context)

                        pass

                    elif item_type == 'NODEGROUP':
                        if subtype == 'ShaderNodeTree':
                            if context.active_object:
                                if not context.active_object.active_material:
                                    context.active_object.active_material = bpy.data.materials.new(name='Material')
                                    context.active_object.active_material.use_nodes = True
                                    for current_node in context.active_object.active_material.node_tree.nodes:
                                        if current_node.bl_idname != 'ShaderNodeOutputMaterial':
                                            context.active_object.active_material.node_tree.nodes.remove(current_node)
                        active_node_tree = __class__.active_node_tree(context=context)
                        if node_in_json and active_node_tree:
                            nodegroup = __class__.json_to_node_group(active_node_tree, node_in_json)
                            if nodegroup:
                                nodegroup['bis_uid'] = bis_item_id
            else:
                request_rez['data']['text'] = 'BIS server not request'
        return request_rez

    @staticmethod
    def to_bis(context, item, item_type, tags=''):
        # item = material or nodegroup
        # item_type = 'MATERIAL' or 'NODEGROUP'
        request_rez = {"stat": "ERR", "data": {"text": "Error to save"}}
        item_json = None
        if item:
            if item_type == 'MATERIAL':
                item_json = Material.to_json(context=context, material=item)
            elif item_type == 'NODEGROUP' and item.type == 'GROUP':
                    item_json = __class__.node_group_to_json(nodegroup=item)
        if cfg.to_server_to_file:
            with open(os.path.join(os.path.dirname(bpy.data.filepath), 'send_to_server.json'), 'w') as currentFile:
                json.dump(item_json, currentFile, indent=4)
        # send to server
        if item_json and not cfg.no_sending_to_server:
            bis_links = list(__class__.get_bis_linked_items('bis_linked_item', item_json))
            request = WebRequest.send_request({
                'for': 'add_item',
                'item_body': json.dumps(item_json),
                'storage': __class__.storage_type(context=context),
                'storage_subtype': __class__.get_subtype(context=context),
                'storage_subtype2': __class__.get_subtype2(context=context),
                'procedural': 1 if __class__.is_procedural(material=item) else 0,
                'engine': context.window.scene.render.engine,
                'bis_links': json.dumps(bis_links),
                'item_name': item_json['name'],
                'item_tags': tags.strip(),
                'addon_version': Addon.current_version()
            })
            if request:
                request_rez = json.loads(request.text)
        if request_rez['stat'] == 'OK':
            item['bis_uid'] = request_rez['data']['id']
        return request_rez

    @staticmethod
    def update_in_bis(context, item, item_type):
        # item = material or nodegroup
        # item_type = 'MATERIAL' or 'NODEGROUP'
        request_rez = {"stat": "ERR", "data": {"text": "Error to update"}}
        item_json = None
        if item:
            if 'bis_uid' in item:
                if item_type == 'MATERIAL':
                    item_json = Material.to_json(context=context, material=item)
                elif item_type == 'NODEGROUP' and item.type == 'GROUP':
                    item_json = __class__.node_group_to_json(item)
            else:
                request_rez['data']['text'] = 'Save this Material item to the BIS first!'
        else:
            request_rez['data']['text'] = 'Undefined material item to update'
        if cfg.to_server_to_file:
            with open(os.path.join(os.path.dirname(bpy.data.filepath), 'send_to_server.json'), 'w') as currentFile:
                json.dump(item_json, currentFile, indent=4)
        # send to server
        if item_json and not cfg.no_sending_to_server:
            bis_links = list(__class__.get_bis_linked_items('bis_linked_item', item_json))
            request = WebRequest.send_request(data={
                'for': 'update_item',
                'item_body': json.dumps(item_json),
                'storage': __class__.storage_type(context=context),
                'storage_subtype': __class__.get_subtype(context=context),
                'storage_subtype2': __class__.get_subtype2(context=context),
                'procedural': 1 if __class__.is_procedural(material=item) else 0,
                'engine': context.window.scene.render.engine,
                'bis_links': json.dumps(bis_links),
                'item_id': item['bis_uid'],
                'item_name': item_json['name'],
                'addon_version': Addon.current_version()
            })
            if request:
                request_rez = json.loads(request.text)
        return request_rez

    @staticmethod
    def node_group_to_json(nodegroup):
        # convert node group to json
        group_in_json = None
        if nodegroup.type == 'GROUP':
            nodegroup_class = 'Node' + nodegroup.bl_idname
            if hasattr(sys.modules[__name__], nodegroup_class):
                group_in_json = getattr(sys.modules[__name__], nodegroup_class).node_to_json(nodegroup)
        return group_in_json

    @staticmethod
    def json_to_node_group(dest_nodetree, node_in_json):
        # recreate node group from json
        if cfg.from_server_to_file:
            with open(os.path.join(os.path.dirname(bpy.data.filepath), 'received_from_server.json'), 'w') as currentFile:
                json.dump(node_in_json, currentFile, indent=4)
        current_node = None
        if dest_nodetree:
            # for older compatibility (v 1.4.1)
            # if all node groups becomes 1.4.2. and later - remove all "else" condition
            node_group_version = node_in_json['BIS_addon_version'] if 'BIS_addon_version' in node_in_json else Addon.node_group_first_version
            if Addon.node_group_version_higher(node_group_version, Addon.current_version()):
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message='This node group was saved in higher BIS version and may not load correctly.\
                 Please download the last BIS add-on version!')
            if Addon.node_group_version_higher(node_group_version, Addon.node_group_first_version):
                # 1.4.2
                node_class = getattr(sys.modules[__name__], 'Node' + node_in_json['bl_idname'])
            else:
                # 1.4.1
                node_class = getattr(sys.modules[__name__], 'NodeBase' + node_in_json['bl_type'])
            current_node = node_class.json_to_node(node_tree=dest_nodetree, node_json=node_in_json)
            current_node.location = (0, 0)
        return current_node

    @staticmethod
    def storage_type(context):
        # return context.area.spaces.active.type
        return 'NODE_EDITOR'

    @staticmethod
    def get_subtype(context):
        # return subtype
        if context.area.spaces.active.type == 'NODE_EDITOR':
            return context.area.spaces.active.tree_type
        else:
            return 'ShaderNodeTree'

    @staticmethod
    def get_subtype2(context):
        # return subtype2
        if context.area.spaces.active.type == 'NODE_EDITOR':
            return context.area.spaces.active.shader_type
        else:
            return 'OBJECT'

    @staticmethod
    def active_node_tree(context):
        # returns currently opened node tree in NODE_EDITOR window
        active_node_tree = None
        subtype = __class__.get_subtype(context=context)
        if subtype == 'ShaderNodeTree':
            subtype2 = __class__.get_subtype2(context=context)
            if subtype2 == 'OBJECT':
                if context.active_object and context.active_object.active_material:
                    active_node_tree = context.active_object.active_material.node_tree
            elif subtype2 == 'WORLD':
                active_node_tree = context.scene.world.node_tree
        elif subtype == 'CompositorNodeTree':
            if context.window.scene.use_nodes:
                active_node_tree = context.area.spaces.active.node_tree
        if active_node_tree and hasattr(context.space_data, 'path'):
            for i in range(len(context.space_data.path) - 1):
                active_node_tree = active_node_tree.nodes.active.node_tree
        return active_node_tree

    @staticmethod
    def active_node(context):
        # returns currently active node in NODE_EDITOR window
        active_node = None
        active_node_tree = __class__.active_node_tree(context=context)
        if active_node_tree:
            active_node = active_node_tree.nodes.active
        return active_node

    @staticmethod
    def active_material(context):
        # returns currently active material in NODE_EDITOR window
        active_material = None
        if context.active_object and context.active_object.active_material:
            active_material = context.active_object.active_material
        return active_material

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
    # returns generator to crate list with all linked items (texts, ...) to current item (nodegroup)
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
