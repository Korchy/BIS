# Nikita Akimov
# interplanety@interplanety.org

# Blender types to/from JSON conversion
# Blender types with prefix BL

import os
import sys
from typing import Dict, Any
import bpy


class BLbpy_prop_collection:

    @classmethod
    def to_json(cls, instance):
        # instance to json call
        instance_in_json = cls._instance_to_json(collection=instance)
        return instance_in_json

    @classmethod
    def from_json(cls, node, collection, json):
        # instance from json call
        return cls._json_to_instance(node=node, collection=collection, json=json)

    @classmethod
    def _instance_to_json(cls, collection):
        collection_in_json = []
        for key, instance in collection.items():
            instance_conversion_class = BLBaseType
            if hasattr(sys.modules[__name__], 'BL' + type(instance).__name__):
                # has class for conversion
                instance_conversion_class = getattr(sys.modules[__name__], 'BL' + type(instance).__name__)
            collection_item_in_json = instance_conversion_class.to_json(instance=instance)
            collection_in_json.append(collection_item_in_json)
        return collection_in_json

    @classmethod
    def _json_to_instance(cls, node, collection, json):
        # data from json
        for i, collection_item_in_json in enumerate(json):
            instance_conversion_class = None
            if hasattr(sys.modules[__name__], 'BL' + collection_item_in_json['class']):
                instance_conversion_class = getattr(sys.modules[__name__], 'BL' + collection_item_in_json['class'])
            if instance_conversion_class:
                if len(collection) <= i and hasattr(instance_conversion_class, 'new_item'):
                    instance_conversion_class.new_item(node)
                if len(collection) > i:
                    instance_conversion_class.from_json(collection[i], collection_item_in_json)
        return collection


class BLBaseType:

    @classmethod
    def to_json(cls, instance) -> Dict[str, Any]:
        # instance to json call
        instance_in_json = {
            'class': type(instance).__name__,
            'instance': cls._instance_to_json(instance=instance)
        }
        return instance_in_json

    @classmethod
    def from_json(cls, instance, json, instance_field=None):
        # instance from json call
        return cls._json_to_instance(instance=instance, json=json['instance'], instance_field=instance_field)

    @classmethod
    def _instance_to_json(cls, instance):
        # get data from instance and convert them to json
        json = {}
        return json

    @classmethod
    def _json_to_instance(cls, instance, json, instance_field=None):
        # get data from json and fill instance with that data
        return instance


class BLImageFormatSettings(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {
            'cineon_black': instance.cineon_black,
            'cineon_gamma': instance.cineon_gamma,
            'cineon_white': instance.cineon_white,
            'color_depth': instance.color_depth,
            'color_mode': instance.color_mode,
            'compression': instance.compression,
            'exr_codec': instance.exr_codec,
            'file_format': instance.file_format,
            'jpeg2k_codec': instance.jpeg2k_codec,
            'quality': instance.quality,
            'tiff_codec': instance.tiff_codec,
            'use_cineon_log': instance.use_cineon_log,
            'use_jpeg2k_cinema_48': instance.use_jpeg2k_cinema_48,
            'use_jpeg2k_cinema_preset': instance.use_jpeg2k_cinema_preset,
            'use_jpeg2k_ycc': instance.use_jpeg2k_ycc,
            'use_preview': instance.use_preview,
            'use_zbuffer': instance.use_zbuffer,
            'views_format': instance.views_format
        }
        return json

    @classmethod
    def _json_to_instance(cls, instance, json, instance_field=None):
        # data from json
        instance.file_format = json['file_format']
        instance.cineon_black = json['cineon_black']
        instance.cineon_gamma = json['cineon_gamma']
        instance.cineon_white = json['cineon_white']
        instance.color_depth = json['color_depth']
        instance.color_mode = json['color_mode']
        instance.compression = json['compression']
        instance.exr_codec = json['exr_codec']
        instance.jpeg2k_codec = json['jpeg2k_codec']
        instance.quality = json['quality']
        instance.tiff_codec = json['tiff_codec']
        instance.use_cineon_log = json['use_cineon_log']
        instance.use_jpeg2k_cinema_48 = json['use_jpeg2k_cinema_48']
        instance.use_jpeg2k_cinema_preset = json['use_jpeg2k_cinema_preset']
        instance.use_jpeg2k_ycc = json['use_jpeg2k_ycc']
        instance.use_preview = json['use_preview']
        instance.use_zbuffer = json['use_zbuffer']
        instance.views_format = json['views_format']
        return instance
    
    
class BLNodeOutputFileSlotFile(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {
            'format': BLImageFormatSettings.to_json(instance.format),
            'path': instance.path,
            'use_node_format': instance.use_node_format
        }
        return json

    @classmethod
    def _json_to_instance(cls, instance, json, instance_field=None):
        # data from json
        BLImageFormatSettings.from_json(instance.format, json['format'])
        instance.path = json['path']
        instance.use_node_format = json['use_node_format']
        return instance

    @classmethod
    def new_item(cls, node):
        # creates new real item
        context_copy = bpy.context.copy()
        context_copy['node'] = node
        bpy.ops.node.output_file_add_socket(context_copy)


class BLColor(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {
            'r': instance.r,
            'g': instance.g,
            'b': instance.b
        }
        return json

    @classmethod
    def _json_to_instance(cls, instance, json, instance_field=None):
        # data from json
        instance.r = json['r']
        instance.g = json['g']
        instance.b = json['b']
        return instance


class BLVector(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {
            'x': instance.x,
            'y': instance.y,
            'z': instance.z
        }
        return json

    @classmethod
    def _json_to_instance(cls, instance, json, instance_field=None):
        # data from json
        instance.x = json['x']
        instance.y = json['y']
        instance.z = json['z']
        return instance


class BLbpy_prop_array:

    @classmethod
    def to_json(cls, prop_array):
        # instance to json call
        instance_in_json = []
        for prop in prop_array:
            instance_in_json.append(prop)
        return instance_in_json

    @classmethod
    def from_json(cls, prop_array, json):
        # instance from json call
        for i, prop in enumerate(json):
            prop_array[i] = prop


class BLset:

    @classmethod
    def to_json(cls, instance):
        # instance to json call
        return list(instance)

    @classmethod
    def from_json(cls, json):
        # instance from json call
        return set(json)


class BLObject(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {}
        if instance:
            json['name'] = instance.name
        return json

    @classmethod
    def _json_to_instance(cls, instance, json, instance_field=None):
        # data from json
        if 'name' in json and json['name'] in bpy.data.objects:
            instance.object = bpy.data.objects[json['name']]
        return instance


class BLCacheFile(BLBaseType):

    @classmethod
    def _instance_to_json(cls, instance):
        # data to json
        json = {}
        if instance:
            json['name'] = instance.name
            json['filepath'] = os.path.normpath(os.path.join(os.path.dirname(bpy.data.filepath), instance.filepath.replace('//', '')))
        return json

    @classmethod
    def _json_to_instance(cls, instance, json, instance_field=None):
        # data from json
        if 'name' in json:
            if json['name'] not in bpy.data.cache_files:
                if 'filepath' in json and json['filepath']:
                    bpy.ops.cachefile.open(filepath=json['filepath'])
            if json['name'] in bpy.data.cache_files:
                if instance_field:
                    setattr(instance, instance_field, bpy.data.cache_files[json['name']])
        return instance
