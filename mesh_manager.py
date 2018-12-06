# Nikita Akimov
# interplanety@interplanety.org

import json
import tempfile
import zipfile
import os
import bpy
from .WebRequests import WebRequest
from .BIS_Items import BIS_Items
from .addon import Addon
from . import cfg


class MeshManager:

    _mesh_limit_vert_count = 50000      # max number of vertices im mesh
    _mesh_limit_file_size = 3145728     # max exported to obj and zipped file size (3 Mb)

    @staticmethod
    def items_from_bis(context, search_filter, page, update_preview):
        # get page of items list from BIS
        rez = None
        request = WebRequest.send_request({
            'for': 'get_items',
            'search_filter': search_filter,
            'page': page,
            'storage': __class__.storage_type(context),
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
                        'storage': __class__.storage_type(context)
                    })
                    if request:
                        previews_update_rez = json.loads(request.text)
                        if previews_update_rez['stat'] == 'OK':
                            BIS_Items.updatePreviewsFromData(previews_update_rez['data']['items'], __class__.storage_type(context))
                BIS_Items.createItemsList(request_rez['data']['items'], __class__.storage_type(context))
                context.window_manager.bis_get_meshes_info_from_storage_vars.current_page = page
                context.window_manager.bis_get_meshes_info_from_storage_vars.current_page_status = request_rez['data']['status']
        return rez

    @staticmethod
    def storage_type(context=None):
        if context:
            return context.area.spaces.active.type
        else:
            return 'VIEW_3D'

    @staticmethod
    def to_bis(mesh_list=[], name='', tags=''):
        rez = {"stat": "ERR", "data": {"text": "Error to save"}}
        if mesh_list:
            if not name:
                name = mesh_list[0].name
            mesh_in_json = {
                'obj_file_name': name
            }
            with tempfile.TemporaryDirectory() as temp_dir:
                mesh_obj_path = __class__.export_to_obj(mesh_list=mesh_list, name=name, export_to=temp_dir)
                if mesh_obj_path and os.path.exists(mesh_obj_path):
                    tags += (';' if tags else '') + '{0[0]}.{0[1]}'.format(bpy.app.version)
                    request = WebRequest.send_request(data={
                        'for': 'add_item',
                        'storage': __class__.storage_type(),
                        'item_body': json.dumps(mesh_in_json),
                        'item_name': name,
                        'item_tags': tags,
                        'addon_version': Addon.current_version()
                    }, files={
                        'mesh_file': open(mesh_obj_path, 'rb')
                    })
                    if request:
                        rez = json.loads(request.text)
                        if rez['stat'] == 'OK':
                            for mesh in mesh_list:
                                mesh['bis_uid'] = rez['data']['id']
                        else:
                            bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['stat'] + ': ' + rez['data']['text'])
        else:
            rez['data']['text'] = 'No mesh to save'
        return rez

    @staticmethod
    def from_bis(context, bis_item_id):
        rez = {"stat": "ERR", "data": {"text": "No Id", "content": None}}
        if bis_item_id:
            request = WebRequest.send_request({
                'for': 'get_item',
                'storage': __class__.storage_type(),
                'id': bis_item_id
            })
            if request:
                request_rez = json.loads(request.text)
                if request_rez['stat'] == 'OK':
                    item_in_json = json.loads(request_rez['data']['item'])
                    if 'file_attachment' in item_in_json and 'link_type' in item_in_json['file_attachment']:
                        with tempfile.TemporaryDirectory() as temp_dir:
                            if item_in_json['file_attachment']['link_type'] == 'internal':
                                request_file = WebRequest.send_request({
                                    'for': 'get_item_file_attachment',
                                    'storage': __class__.storage_type(),
                                    'id': bis_item_id
                                })
                                if request_file:
                                    zip_file_name = str(bis_item_id) + '.zip'
                                    zip_file_path = os.path.join(temp_dir, zip_file_name)
                                    with open(zip_file_path, 'wb') as temp_item_file_attachment:
                                        temp_item_file_attachment.write(request_file.content)
                                        if cfg.from_server_to_file:
                                            from shutil import copyfile
                                            copyfile(zip_file_path, os.path.join(os.path.dirname(bpy.data.filepath), zip_file_name))
                                        __class__.import_from_obj(context, zip_file_path, obj_file_name=item_in_json['obj_file_name'])
                            elif item_in_json['file_attachment']['link_type'] == 'external':
                                # external links - not supports at present
                                pass
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT',  message=rez['stat'] + ': ' + rez['data']['text'])
        return rez

    @staticmethod
    def export_to_obj(mesh_list, name, export_to):
        # saves mesh to the export_to directory in obj format and zip it. Returns full path to file.
        rez = None
        if mesh_list:
            vertices_in_meshes = 0
            for mesh in mesh_list:
                vertices_in_meshes += len(mesh.data.vertices)
            if vertices_in_meshes <= __class__._mesh_limit_vert_count:
                obj_file_name = name + '.obj'
                obj_file_path = os.path.join(export_to, obj_file_name)
                bpy.ops.export_scene.obj(
                    filepath=obj_file_path,
                    check_existing=False,
                    use_selection=True,
                    use_mesh_modifiers=False,
                    use_edges=False,
                    use_normals=False,
                    use_uvs=True,
                    use_materials=False
                )
                if os.path.exists(obj_file_path):
                    zip_file_name = name + '.zip'
                    zip_file_path = os.path.join(export_to, zip_file_name)
                    zip_file = zipfile.ZipFile(zip_file_path, 'w')
                    zip_file.write(obj_file_path, compress_type=zipfile.ZIP_DEFLATED, arcname=obj_file_name)
                    zip_file.close()
                    if os.path.exists(zip_file_path):
                        if cfg.to_server_to_file:
                            from shutil import copyfile
                            copyfile(zip_file_path, os.path.join(os.path.dirname(bpy.data.filepath), zip_file_name))
                        if os.stat(zip_file_path).st_size < __class__._mesh_limit_file_size:
                            rez = zip_file_path
                        else:
                            bpy.ops.message.messagebox('INVOKE_DEFAULT', message='ERR: Saving meshes must be less 3 Mb after zip export')
            else:
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message='ERR: Saving meshes must be less 50 000 vertices at all')
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message='ERR: No meshes to save')
        return rez

    @staticmethod
    def import_from_obj(context, zip_fipe_path, obj_file_name):
        # add meshes to scene from zipped archive with obj file
        if context.active_object and context.active_object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
        for mesh in context.selected_objects:
            mesh.select = False
        if os.path.exists(zip_fipe_path):
            obj_file_path = os.path.dirname(zip_fipe_path)
            obj_file_name = os.path.join(obj_file_path, obj_file_name + '.obj')
            zip_file = zipfile.ZipFile(file=zip_fipe_path)
            zip_file.extractall(path=obj_file_path)
            if os.path.exists(obj_file_name):
                bpy.ops.import_scene.obj(
                    filepath=obj_file_name,
                    use_image_search=False
                )
