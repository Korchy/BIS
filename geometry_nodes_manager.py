# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


import bpy
import json
import os
from shutil import copyfile
import tempfile
from . import cfg
from .addon import Addon
from .bis_items import BISItems
from .file_manager import FileManager
from .blender_ex import BlenderEx
from .bpy_plus.names import Names
from .data_block_manager import DataBlockManager
from .material import Material
from .node_tree import NodeTree
from .WebRequests import WebRequest, WebAuthVars


class GeometryNodesManager(DataBlockManager):

    # Geometry Nodes

    _limit_file_size = 3*1024*1024     # max exported to .blend and zipped file size (3 Mb)
    _storage_type = 'NODE_EDITOR'

    @classmethod
    def items_from_bis(cls, context, search_filter, page, update_preview):
        # get page of items list from BIS
        rez = None
        storage_subtype = Material.get_subtype(context)     # GeometryNodeTree
        storage_subtype2 = Material.get_subtype2(context)   # OBJECT
        request = WebRequest.send_request(
            context=context,
            data={
                'for': 'get_items',
                'search_filter': search_filter,
                'page': page,
                'storage': cls._storage_type,
                'storage_subtype': storage_subtype,
                'storage_subtype2': storage_subtype2,
                'update_preview': update_preview,
                'addon_version': Addon.current_version()
            }
        )
        if request:
            request_rez = json.loads(request.text)
            rez = request_rez['stat']
            if request_rez['stat'] == 'OK':
                if not request_rez['data']['items']:
                    if WebAuthVars.userProStatus:
                        bpy.ops.bis.messagebox(
                            'INVOKE_DEFAULT',
                            message='Nothing found'
                        )
                    else:
                        bpy.ops.bis.messagebox(
                            'INVOKE_DEFAULT',
                            message='You do not have any active geometry nodes.\n \
                            Please log in your account on the BIS web site,\n \
                            Add some meshes to the active palette,\n \
                            And press this button again.'
                        )
                preview_to_update = BISItems.update_previews_from_data(
                    data=request_rez['data']['items'],
                    list_name=cls._storage_type
                )
                if preview_to_update:
                    request = WebRequest.send_request(
                        context=context,
                        data={
                            'for': 'update_previews',
                            'preview_list': preview_to_update,
                            'storage': cls._storage_type,
                            'storage_subtype': storage_subtype,
                            'storage_subtype2': storage_subtype2,
                            'addon_version': Addon.current_version()
                        }
                    )
                    if request:
                        previews_update_rez = json.loads(request.text)
                        if previews_update_rez['stat'] == 'OK':
                            BISItems.update_previews_from_data(
                                data=previews_update_rez['data']['items'],
                                list_name=cls._storage_type
                            )
                BISItems.create_items_list(
                    data=request_rez['data']['items'],
                    list_name=cls._storage_type
                )
                context.window_manager.bis_get_meshes_info_from_storage_vars.current_page = page
                context.window_manager.bis_get_meshes_info_from_storage_vars.current_page_status = \
                    request_rez['data']['status']
        return rez

    @classmethod
    def from_bis(cls, context, bis_item_id, item_type):
        # item_type = 'MATERIAL' or 'NODEGROUP'
        request_rez = {'stat': 'ERR', 'data': {'text': 'No Id', 'content': None}}
        if bis_item_id:
            request = WebRequest.send_request(
                context=context,
                data={
                    'for': 'get_item',
                    'storage': cls._storage_type,
                    'storage_subtype': Material.get_subtype(context),
                    'storage_subtype2': Material.get_subtype2(context),
                    'id': bis_item_id,
                    'addon_version': Addon.current_version()
                }
            )
            if request:
                request_rez = json.loads(request.text)
                if request_rez['stat'] == 'OK':
                    item_in_json = json.loads(request_rez['data']['item'])
                    if 'file_attachment' in request_rez['data'] and request_rez['data']['file_attachment']:
                        with tempfile.TemporaryDirectory() as temp_dir:
                            request_file = WebRequest.send_request(
                                context=context,
                                data={
                                    'for': 'get_item_file_attachment',
                                    'storage': cls._storage_type,
                                    'id': bis_item_id
                                }
                            )
                            if request_file:
                                zip_file_name = str(bis_item_id) + '.zip'
                                zip_file_path = os.path.join(temp_dir, zip_file_name)
                                with open(zip_file_path, 'wb') as temp_item_file_attachment:
                                    temp_item_file_attachment.write(request_file.content)
                                # to file (debug)
                                FileManager.from_server_to_file(
                                    json_data=item_in_json,
                                    attachment_file_path=zip_file_path
                                )
                                # if cfg.from_server_to_file:
                                #     copyfile(
                                #         zip_file_path,
                                #         os.path.join(FileManager.project_dir(), zip_file_name)
                                #     )
                                #     with open(os.path.join(FileManager.project_dir(),
                                #                            'received_from_server.json'), 'w') as currentFile:
                                #         json.dump(item_in_json, currentFile, indent=4)
                                if os.path.exists(zip_file_path):
                                    # if already exists node group with the same name - rename it
                                    if item_in_json['data_block_name'] in context.blend_data.node_groups:
                                        context.blend_data.node_groups[item_in_json['data_block_name']].name = \
                                            Names.increase(name=item_in_json['data_block_name'])
                                    # import from attachment .blend file
                                    imported_data_block_names = cls.import_from_blend(
                                        context=context,
                                        zip_file_path=zip_file_path,
                                        file_name=item_in_json['data_block_name'],
                                        data_block_type=item_in_json['data_block_type'],
                                        data_block_name=item_in_json['data_block_name']
                                    )
                                    geometry_node_tree = next(tree for tree in context.blend_data.node_groups
                                                              if tree.name in imported_data_block_names)
                                    if geometry_node_tree:
                                        geometry_node_tree['bis_uid'] = bis_item_id
                                        # add to active object geometry nodes modifier
                                        gn_modifier = cls.active_gn_modifier(
                                            context=context,
                                            obj=context.active_object
                                        )
                                        if not gn_modifier:
                                            gn_modifier = cls.new_gn_modifier(
                                                obj=context.active_object
                                            )
                                        if item_type == 'MATERIAL':
                                            # fully replace modifier node tree
                                            gn_modifier.node_group = geometry_node_tree
                                        elif item_type == 'NODEGROUP':
                                            # just add as separate node group to the current modifier node tree
                                            node_group = gn_modifier.node_group.nodes.new(
                                                type='GeometryNodeGroup'
                                            )
                                            node_group.node_tree = geometry_node_tree
                                            node_group.location = (0.0, 0.0)
        else:
            bpy.ops.bis.messagebox(
                'INVOKE_DEFAULT',
                message=request_rez['stat'] + ': ' + request_rez['data']['text']
            )
        return request_rez

    @classmethod
    def to_bis(cls, context, node_tree_container, tags=''):
        request_rez = {'stat': 'ERR', 'data': {'text': 'Error to save'}}
        if node_tree_container:
            name = cls._gn_name(node_tree_container=node_tree_container)
            # store node tree anyway
            data_block = cls.node_tree(node_tree_container=node_tree_container)
            data_in_json = {
                'data_block_type': 'node_groups',
                'data_block_name': name
            }
            with tempfile.TemporaryDirectory() as temp_dir:
                attachments_path = cls.export_to_blend(
                    context=context,
                    data_block={data_block},
                    export_path=temp_dir,
                    export_file_name=name
                )
                if attachments_path and os.path.exists(attachments_path):
                    tags += (';' if tags else '') + ';'.join(cls.tags(node_tree_container=node_tree_container))
                    if not cfg.no_sending_to_server:
                        request = WebRequest.send_request(
                            context=context,
                            data={
                                'for': 'add_item',
                                'storage': cls._storage_type,
                                'storage_subtype': Material.get_subtype(context=context),
                                'storage_subtype2': Material.get_subtype2(context=context),
                                'item_body': json.dumps(data_in_json),
                                'item_name': name,
                                'item_tags': tags.strip(),
                                'procedural': 1 if NodeTree.is_procedural(
                                    node_tree=cls.node_tree(node_tree_container=node_tree_container)) else 0,
                                'addon_version': Addon.current_version(),
                                'blender_version': BlenderEx.version_str_short()
                            },
                            files={
                                'attachment_file': open(attachments_path, 'rb')
                            }
                        )
                        if request:
                            request_rez = json.loads(request.text)
                            if request_rez['stat'] == 'OK':
                                data_block['bis_uid'] = request_rez['data']['id']
            # to file (debug)
            if cfg.to_server_to_file:
                with open(os.path.join(FileManager.project_dir(), 'send_to_server.json'), 'w') as currentFile:
                    json.dump(data_in_json, currentFile, indent=4)
        else:
            request_rez['data']['text'] = 'No data to save'
        return request_rez

    @classmethod
    def update_in_bis(cls, context, node_tree_container):
        # update current geometry node tree
        request_rez = {"stat": "ERR", "data": {"text": "Error to update"}}
        if node_tree_container:
            name = cls._gn_name(node_tree_container=node_tree_container)
            gn_node_tree = cls.node_tree(node_tree_container=node_tree_container)
            bis_uid = None
            if gn_node_tree:
                if 'bis_uid' in gn_node_tree and gn_node_tree['bis_uid']:
                    bis_uid = gn_node_tree['bis_uid']
                else:
                    request_rez['data']['text'] = 'Save this GN item to the BIS first!'
            else:
                request_rez['data']['text'] = 'Undefined GN item to update'
            if bis_uid:
                data_in_json = {
                    'data_block_type': 'node_groups',
                    'data_block_name': name
                }
                with tempfile.TemporaryDirectory() as temp_dir:
                    attachments_path = cls.export_to_blend(
                        context=context,
                        data_block={gn_node_tree},
                        export_path=temp_dir,
                        export_file_name=name
                    )
                    if attachments_path and os.path.exists(attachments_path):
                        # send to server
                        # save to file (debug)
                        FileManager.to_server_to_file(
                            json_data=data_in_json,
                            attachment_file_path=attachments_path
                        )
                        # send request
                        if not cfg.no_sending_to_server:
                            request = WebRequest.send_request(
                                context=context,
                                data={
                                    'for': 'update_item',
                                    'storage': cls._storage_type,
                                    'storage_subtype': Material.get_subtype(context=context),
                                    'storage_subtype2': Material.get_subtype2(context=context),
                                    'item_id': bis_uid,
                                    'item_body': json.dumps(data_in_json),
                                    'item_name': name,
                                    'procedural': 1 if NodeTree.is_procedural(
                                        node_tree=cls.node_tree(node_tree_container=node_tree_container)) else 0,
                                    'addon_version': Addon.current_version(),
                                    'blender_version': BlenderEx.version_str_short()
                                },
                                files={
                                    'attachment_file': open(attachments_path, 'rb')
                                }
                            )
                            if request:
                                request_rez = json.loads(request.text)
        else:
            request_rez['data']['text'] = 'Cant get object to update - no active object from BIS'
        return request_rez

    @staticmethod
    def node_tree(node_tree_container):
        # get node tree from container
        node_tree = None
        if node_tree_container.type == 'GROUP':
            node_tree = node_tree_container.node_tree
        elif node_tree_container.type == 'NODES':
            node_tree = node_tree_container.node_group
        return node_tree

    @classmethod
    def tags(cls, node_tree_container):
        # additional tags for geometry nodes
        tags = {'geometry nodes', BlenderEx.version_str_short()}
        if NodeTree.is_procedural(node_tree=cls.node_tree(node_tree_container=node_tree_container)):
            tags.add('procedural')
        return tags

    @staticmethod
    def _gn_name(node_tree_container):
        # name
        name = ''
        if node_tree_container.type == 'GROUP':
            name = node_tree_container.node_tree.name
        elif node_tree_container.type == 'NODES':
            name = node_tree_container.node_group.name
        name = ''.join((x if x.isalnum() else '_' for x in name))
        return name

    @staticmethod
    def new_gn_modifier(obj):
        # add new geometry nodes modifier for object
        gn = obj.modifiers.new(
            type='NODES',
            name='Geometry Nodes'
        )
        return gn

    @staticmethod
    def new_gn_node_tree(context):
        # create new geometry node tree
        gn_node_tree = context.blend_data.node_groups.new(
            type='GeometryNodeTree',
            name='Geometry Nodes'
        )
        return gn_node_tree

    @classmethod
    def active_gn_modifier(cls, context, obj):
        # get active geometry nodes modifier from object
        gn_modifier = next((modifier for modifier in obj.modifiers
                            if modifier.type == 'NODES' and modifier == obj.modifiers.active), None)
        if gn_modifier and not gn_modifier.node_group:
            gn_modifier.node_group = cls.new_gn_node_tree(
                context=context
            )
        return gn_modifier
