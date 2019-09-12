# Nikita Akimov
# interplanety@interplanety.org

import bpy
import os
import base64
import bpy.utils.previews


class BISItems:

    items_lists = {}

    @classmethod
    def register(cls):
        cls.items_lists['NODE_EDITOR'] = bpy.utils.previews.new()
        cls.items_lists['NODE_EDITOR'].items = []
        cls.items_lists['TEXT_EDITOR'] = bpy.utils.previews.new()
        cls.items_lists['TEXT_EDITOR'].items = []
        cls.items_lists['VIEW_3D'] = bpy.utils.previews.new()
        cls.items_lists['VIEW_3D'].items = []

    @classmethod
    def unregister(cls):
        for item_list in cls.items_lists.values():
            item_list.items.clear()
            bpy.utils.previews.remove(item_list)
        cls.items_lists.clear()

    @classmethod
    def create_items_list(cls, data, list_name, previews=True):
        cls.clear_items_list(list_name)
        for item_info in data:
            if previews:
                path = cls.get_preview_path(item_id=int(item_info['id']), list_name=list_name)
                thumb = cls.items_lists[list_name].load(path, path, 'IMAGE')
                cls.items_lists[list_name].items.append((item_info['id'], item_info['name'], item_info['name'], thumb.icon_id, int(item_info['id'])))
            else:
                cls.items_lists[list_name].items.append((item_info['id'], item_info['name'], item_info['name'], '', int(item_info['id'])))

    @classmethod
    def get_previews(cls, storage_type):
        if storage_type:
            return cls.items_lists[storage_type].items
        else:
            return []

    @classmethod
    def clear_items_list(cls, name):
        cls.items_lists[name].clear()
        cls.items_lists[name].items.clear()

    @staticmethod
    def get_preview_relative_dir(item_id, list_name):
        item_dir = 0
        while item_id > item_dir:
            item_dir += 1000
        return 'previews' + os.path.sep + list_name + os.path.sep + str(item_dir - (0 if item_dir == 0 else 1000)) + '-' + str(item_dir)

    @classmethod
    def get_preview_dir(cls, item_id, list_name):
        return os.path.dirname(__file__) + os.path.sep + cls.get_preview_relative_dir(item_id=item_id, list_name=list_name)

    @classmethod
    def get_preview_path(cls, item_id, list_name):
        return cls.get_preview_dir(item_id=item_id, list_name=list_name) + os.path.sep + str(item_id) + '.jpg'

    @classmethod
    def update_previews_from_data(cls, data, list_name):
        preview_to_update = ''
        for prewiew_info in data:
            preview_dir = cls.get_preview_dir(item_id=int(prewiew_info['id']), list_name=list_name)
            if prewiew_info['preview']:
                preview_content = base64.b64decode(prewiew_info['preview'])
                if not os.path.exists(preview_dir):
                    os.makedirs(preview_dir)
                with open(cls.get_preview_path(item_id=int(prewiew_info['id']), list_name=list_name), 'wb') as current_preview:
                    current_preview.write(preview_content)
            else:
                if not os.path.exists(cls.get_preview_path(item_id=int(prewiew_info['id']), list_name=list_name)):
                    preview_to_update += ('' if preview_to_update == '' else ',') + prewiew_info['id']
        return preview_to_update

    @staticmethod
    def on_preview_select(items_property, storage_type):
        if storage_type == 'NODE_EDITOR':
            bpy.ops.bis.get_nodegroup_from_storage(node_group_id=int(items_property.items))
        elif storage_type == 'TEXT_EDITOR':
            bpy.ops.bis.get_text_from_storage(text_id=int(items_property.items))
        elif storage_type == 'VIEW_3D':
            bpy.ops.bis.get_mesh_from_storage(mesh_id=int(items_property.items))

    # @staticmethod
    # def on_preview_select(self, storage_type):
    #     if storage_type == 'NODE_EDITOR':
    #         bpy.ops.bis.get_nodegroup_from_storage(node_group_id=int(self.items))
    #     elif storage_type == 'TEXT_EDITOR':
    #         bpy.ops.bis.get_text_from_storage(text_id=int(self.items))
    #     elif storage_type == 'VIEW_3D':
    #         bpy.ops.bis.get_mesh_from_storage(mesh_id=int(self.items))
    #
    @classmethod
    def get_item_name_by_id(cls, item_id, storage):
        item_in_list = [item[1] for item in cls.items_lists[storage].items if item[4] == item_id]
        if item_in_list:
            return item_in_list[0]
        else:
            return ''


def register():
    BISItems.register()


def unregister():
    BISItems.unregister()
