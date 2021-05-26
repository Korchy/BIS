# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


import json
import os
import tempfile
import bpy
import zipfile
from shutil import copyfile
from .WebRequests import WebRequest, WebAuthVars
from .bis_items import BISItems
from .addon import Addon
from .file_manager import FileManager
from . import cfg


class MeshManager:

    _mesh_limit_vert_count = 50000      # max number of vertices im mesh
    _mesh_limit_file_size = 3*1024*1024     # max exported to obj and zipped file size (3 Mb)

    @classmethod
    def items_from_bis(cls, context, search_filter, page, update_preview):
        # get page of items list from BIS
        rez = None
        request = WebRequest.send_request(
            context=context,
            data={
                'for': 'get_items',
                'search_filter': search_filter,
                'page': page,
                'storage': cls.storage_type(context=context),
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
                            message='You do not have any active meshes.\n \
                            Please log in your account on the BIS web site,\n \
                            Add some meshes to the active palette,\n \
                            And press this button again.'
                        )
                preview_to_update = BISItems.update_previews_from_data(
                    data=request_rez['data']['items'],
                    list_name=cls.storage_type(context=context)
                )
                if preview_to_update:
                    request = WebRequest.send_request(
                        context=context,
                        data={
                            'for': 'update_previews',
                            'preview_list': preview_to_update,
                            'storage': cls.storage_type(context=context),
                            'addon_version': Addon.current_version()
                        }
                    )
                    if request:
                        previews_update_rez = json.loads(request.text)
                        if previews_update_rez['stat'] == 'OK':
                            BISItems.update_previews_from_data(
                                data=previews_update_rez['data']['items'],
                                list_name=cls.storage_type(context=context)
                            )
                BISItems.create_items_list(
                    data=request_rez['data']['items'],
                    list_name=cls.storage_type(context=context)
                )
                context.window_manager.bis_get_meshes_info_from_storage_vars.current_page = page
                context.window_manager.bis_get_meshes_info_from_storage_vars.current_page_status = \
                    request_rez['data']['status']
        return rez

    @classmethod
    def from_bis(cls, context, bis_item_id):
        rez = {"stat": "ERR", "data": {"text": "No Id", "content": None}}
        if bis_item_id:
            request = WebRequest.send_request(
                context=context,
                data={
                    'for': 'get_item',
                    'storage': cls.storage_type(context=context),
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
                                    'storage': cls.storage_type(context=context),
                                    'id': bis_item_id
                                }
                            )
                            if request_file:
                                zip_file_name = str(bis_item_id) + '.zip'
                                zip_file_path = os.path.join(temp_dir, zip_file_name)
                                with open(zip_file_path, 'wb') as temp_item_file_attachment:
                                    temp_item_file_attachment.write(request_file.content)
                                # to file (debug)
                                if cfg.from_server_to_file:
                                    copyfile(
                                        zip_file_path,
                                        os.path.join(FileManager.project_dir(), zip_file_name)
                                    )
                                    with open(os.path.join(FileManager.project_dir(), 'received_from_server.json'), 'w') as currentFile:
                                        json.dump(item_in_json, currentFile, indent=4)
                                if os.path.exists(zip_file_path):
                                    imported_objects = cls.import_from_blend(
                                        context=context,
                                        zip_file_path=zip_file_path,
                                        file_name=item_in_json['attachment_filename'],
                                        collection_name=item_in_json['name']
                                    )
                                    if imported_objects:
                                        for obj in imported_objects:
                                            obj['bis_uid'] = bis_item_id
        else:
            bpy.ops.bis.messagebox('INVOKE_DEFAULT',  message=rez['stat'] + ': ' + rez['data']['text'])
        return rez

    @classmethod
    def to_bis(cls, context, objects: list, name='', tags=''):
        request_rez = {"stat": "ERR", "data": {"text": "Error to save"}}
        if objects:
            if not name:
                name = objects[0].name
            meshes_in_json = {
                'objects': [],
                'attachment_filename': name
            }
            for obj in objects:
                # remove animation data
                obj.animation_data_clear()
                # mesh to json
                meshes_in_json['objects'].append(obj.name)
            with tempfile.TemporaryDirectory() as temp_dir:
                attachments_path = cls.export_to_blend(
                    context=context,
                    objects=objects,
                    name=name,
                    export_path=temp_dir
                )
                if attachments_path and os.path.exists(attachments_path):
                    tags += (';' if tags else '') + '{0[0]}.{0[1]}'.format(bpy.app.version)
                    request = WebRequest.send_request(
                        context=context,
                        data={
                            'for': 'add_item',
                            'storage': cls.storage_type(context=context),
                            'item_body': json.dumps(meshes_in_json),
                            'item_name': name,
                            'item_tags': tags,
                            'addon_version': Addon.current_version()
                        },
                        files={
                            'attachment_file': open(attachments_path, 'rb')
                        }
                    )
                    if request:
                        request_rez = json.loads(request.text)
                        if request_rez['stat'] == 'OK':
                            for obj in objects:
                                obj['bis_uid'] = request_rez['data']['id']
            # to file (debug)
            if cfg.to_server_to_file:
                with open(os.path.join(FileManager.project_dir(), 'send_to_server.json'), 'w') as currentFile:
                    json.dump(meshes_in_json, currentFile, indent=4)
        else:
            request_rez['data']['text'] = 'No selected mesh to save'
        return request_rez

    @classmethod
    def update_in_bis(cls, context, objects: list, bis_uid):
        # update objects by active object (get bis_uid from active object and update it for all selection)
        request_rez = {"stat": "ERR", "data": {"text": "Error to update"}}
        if objects and bis_uid:
            name = objects[0].name  # name not updated but need for make file with attachments
            meshes_in_json = {
                'objects': [],
                'attachment_filename': name
            }
            for obj in objects:
                # remove animation data
                obj.animation_data_clear()
                # mesh to json
                meshes_in_json['objects'].append(obj.name)
            with tempfile.TemporaryDirectory() as temp_dir:
                attachments_path = cls.export_to_blend(
                    context=context,
                    objects=objects,
                    name=name,
                    export_path=temp_dir
                )
                if attachments_path and os.path.exists(attachments_path):
                    request = WebRequest.send_request(
                        context=context,
                        data={
                            'for': 'update_item',
                            'storage': cls.storage_type(context=context),
                            'item_body': json.dumps(meshes_in_json),
                            'item_name': name,
                            'item_id': bis_uid,
                            'addon_version': Addon.current_version()
                        },
                        files={
                            'attachment_file': open(attachments_path, 'rb')
                        }
                    )
                    if request:
                        request_rez = json.loads(request.text)
                        if request_rez['stat'] == 'OK':
                            for obj in objects:
                                obj['bis_uid'] = request_rez['data']['id']
            # to file (debug)
            if cfg.to_server_to_file:
                with open(os.path.join(FileManager.project_dir(), 'send_to_server.json'), 'w') as currentFile:
                    json.dump(meshes_in_json, currentFile, indent=4)
        else:
            request_rez['data']['text'] = 'Cant get object to update - no active object from BIS'
        return request_rez

    @staticmethod
    def storage_type(context=None):
        # return context.area.spaces.active.type
        return 'VIEW_3D'

    @staticmethod
    def get_bis_uid(context):
        # get bis_uid from selected objects
        bis_uid = None
        if context.selected_objects:
            # first bis_uid from selection
            bis_uids = set((obj['bis_uid'] for obj in context.selected_objects if 'bis_uid' in obj))
            if len(bis_uids) == 1:
                # has ths same bis_uid in objects and objects with no bis_uid
                bis_uid = bis_uids.pop()
            elif len(bis_uids) > 1:
                # has several bis_uid in objects - get bis_uid from active object
                active = context.active_object if context.active_object in context.selected_objects else None
                if active and 'bis_uid' in active:
                    bis_uid = active['bis_uid']
        return bis_uid

    @classmethod
    def export_to_blend(cls, context, objects, name, export_path):
        # saves mesh to the export_path directory in a *.blend format and zip it. Returns full path to the file
        rez = None
        if objects:
            if cls._mesh_limit_vert_count >= sum([len(obj.data.vertices) for obj in objects if obj.type == 'MESH']):
                file_name = name + '.blend'
                file_path = os.path.join(export_path, file_name)
                data_blocks = set(objects)
                context.blend_data.libraries.write(file_path, data_blocks)
                if os.path.exists(file_path):
                    zip_file_name = name + '.zip'
                    zip_file_path = os.path.join(export_path, zip_file_name)
                    zip_file = zipfile.ZipFile(zip_file_path, 'w')
                    zip_file.write(
                        filename=file_path,
                        compress_type=zipfile.ZIP_DEFLATED,
                        arcname=file_name
                    )
                    zip_file.close()
                    if os.path.exists(zip_file_path):
                        # to file (debug)
                        if cfg.to_server_to_file:
                            copyfile(
                                zip_file_path,
                                os.path.join(FileManager.project_dir(), zip_file_name)
                            )
                        if os.stat(zip_file_path).st_size < cls._mesh_limit_file_size:
                            rez = zip_file_path
                        else:
                            bpy.ops.bis.messagebox(
                                'INVOKE_DEFAULT',
                                message='ERR: Saving meshes must be less ' +
                                        str(round(cls._mesh_limit_file_size/1024/1024)) +
                                        ' Mb after zip export'
                            )
            else:
                bpy.ops.bis.messagebox(
                    'INVOKE_DEFAULT',
                    message='ERR: Saving meshes must be less ' +
                            str(cls._mesh_limit_vert_count) +
                            ' vertices at all'
                )
        else:
            bpy.ops.bis.messagebox('INVOKE_DEFAULT', message='ERR: No meshes to save')
        return rez

    @classmethod
    def import_from_blend(cls, context, zip_file_path, file_name, collection_name: str):
        # add meshes to scene from zipped archive with *.blend file
        rez = []
        if context.active_object and context.active_object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        cls._deselect_all(context=context)
        # collection
        if collection_name:
            collection = bpy.data.collections.new(name=collection_name)
            context.collection.children.link(collection)
        else:
            collection = context.collection
        # import from file
        if os.path.exists(zip_file_path):
            path = os.path.dirname(zip_file_path)
            full_path = os.path.join(path, file_name + '.blend')
            FileManager.unzip_files(
                source_zip_path=zip_file_path,
                dest_dir=path
            )
            if os.path.exists(full_path):
                with bpy.data.libraries.load(full_path) as (data_from, data_to):
                    data_to.objects = data_from.objects
                for obj in data_to.objects:
                    collection.objects.link(obj)
                rez = data_to.objects[:]
        return rez

    @staticmethod
    def _deselect_all(context):
        # deselect all selected meshes
        for mesh in context.selected_objects:
            mesh.select_set(state=False)
