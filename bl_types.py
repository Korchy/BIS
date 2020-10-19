# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

# Blender types to/from JSON conversion
# Blender types are described with prefix BL

import os
import sys
import bpy
from .TextManager import TextManager
from . import cfg


class BlTypes:

    @classmethod
    def has_json(cls, instance):
        # check if this type described here to get its json
        if hasattr(sys.modules[__name__], 'BL' + instance.__class__.__name__):
            return True
        else:
            return False

    @classmethod
    def to_json(cls, instance, instance_name=None, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # instance to json
        if isinstance(instance, (int, float, bool, set, str)):
            # simple type
            if instance_name:
                return {
                    instance_name: instance
                }
            else:
                return instance
        elif hasattr(sys.modules[__name__], 'BL' + instance.__class__.__name__):
            # complex attribute described in ths module
            instance_class = getattr(sys.modules[__name__], 'BL' + instance.__class__.__name__)
            if instance_name:
                return {
                    instance_name: instance_class.to_json(instance=instance)
                }
            else:
                return instance_class.to_json(instance=instance)
        else:
            # any other complex type - try co process as unknown complex instance
            if cfg.show_debug_err:
                print('Not described in BIS bl_types:')
                print(
                    'instance:', instance, ',',
                    'instance name:', instance_name, ',',
                    'instance class:', instance.__class__.__name__
                )
            if instance_name:
                return {
                    instance_name: BLBaseType.to_json(instance=instance)
                }
            else:
                return BLBaseType.to_json(instance=instance)

    @classmethod
    def complex_to_json(cls, instance, instance_name=None, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        instance_json = {}
        # excluded attributes - don't process them (ex: type, select)
        excluded_attributes = excluded_attributes if excluded_attributes is not None else []
        # first process attributes - need to be processed first because when changed - change another attributes (ex: mode)
        first_attributes = first_attributes if first_attributes is not None else []
        first_attributes_filtered = [
            attr for attr in first_attributes if
            attr not in excluded_attributes
            and hasattr(instance, attr)
            and getattr(instance, attr) is not None  # don't add attributes == None
            and not (isinstance(getattr(instance, attr), str) and not getattr(instance, attr))  # don't add attributes == '' (empty string)
            and (not instance.is_property_readonly(attr) or cls.has_json(instance=getattr(instance, attr)))  # read-only attributes - only complex
        ]
        # get next attributes from instance
        next_attributes_filtered = [
            attr for attr in dir(instance) if
            hasattr(instance, attr)
            and not attr.startswith('__')
            and not attr.startswith('bl_')
            and attr not in excluded_attributes
            and attr not in first_attributes_filtered  # don't add first_attributes_filtered, added them first manually
            and not callable(getattr(instance, attr))
            and getattr(instance, attr) is not None  # don't add attributes == None
            and not (isinstance(getattr(instance, attr), str) and not getattr(instance, attr))  # don't add attributes == '' (empty string)
            and (not instance.is_property_readonly(attr) or cls.has_json(instance=getattr(instance, attr)))  # read-only attributes - only complex
            or attr == 'bl_idname'
        ]
        # all attributes: first - preordered attributes, next - all other attributes
        all_attributes = first_attributes_filtered + next_attributes_filtered
        # get json
        for attr in all_attributes:
            instance_json.update(
                cls.to_json(instance=getattr(instance, attr), instance_name=attr)
            )
        return instance_json

    @classmethod
    def from_json(cls, instance_name, instance_owner, instance_json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # fill instance from json
        if hasattr(instance_owner, instance_name):
            instance = getattr(instance_owner, instance_name)
            # print(
            #     'bltypes attribute - ', 'instance name: ', instance_name, ',',
            #     'instance class', instance.__class__.__name__, ',',
            #     'instance owner', instance_owner, ',',
            #     'instance_json', instance_json
            # )
            if isinstance(instance, (int, float, bool, set, str)):
                # simple type
                setattr(instance_owner, instance_name, instance_json)
                # setattr(instance_owner, instance_name, 'xxx')
            elif hasattr(sys.modules[__name__], 'BL' + instance_json['class']):
                # complex attribute described in ths module
                instance_class = getattr(sys.modules[__name__], 'BL' + instance_json['class'])
                instance_class.from_json(
                    instance_name=instance_name,
                    instance_owner=instance_owner,
                    json=instance_json,
                    attachments_path=attachments_path
                )
            else:
                # any other complex type - try co process as unknown complex instance
                if cfg.show_debug_err:
                    print('Not described in BIS bl_types:')
                    print(
                        'instance name: ', instance_name, ',',
                        'instance class:', instance.__class__.__name__, ',',
                        'instance owner', instance_owner, ',',
                        'instance json:', instance_json
                    )
                BLBaseType.from_json(
                    instance_name=instance_name,
                    instance_owner=instance_owner,
                    json=instance_json,
                    attachments_path=attachments_path,
                    excluded_attributes=excluded_attributes,
                    first_attributes=first_attributes
                )

    @classmethod
    def complex_from_json(cls, instance, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        if instance:
            # instance attributes
            # print(
            #     'bltypes complex attribute - ',
            #     'instance class', instance.__class__.__name__, ',',
            #     'json', json
            # )
            # don't process
            excluded_attributes = excluded_attributes if excluded_attributes is not None else []
            # first attributes - process first because they influence on other attributes
            first_attributes = first_attributes if first_attributes is not None else []
            first_attributes_filtered = [
                attribute_name for attribute_name in json['instance'] if
                attribute_name in first_attributes
            ]
            for attribute_name in first_attributes_filtered:
                if hasattr(instance, attribute_name):
                    cls.from_json(
                        instance_name=attribute_name,
                        instance_owner=instance,
                        instance_json=json['instance'][attribute_name],
                        attachments_path=attachments_path,
                        excluded_attributes=excluded_attributes,
                        first_attributes=first_attributes
                    )
            excluded_attributes += first_attributes_filtered
            # for all other node attributes
            for attribute_name in json['instance']:
                if attribute_name not in excluded_attributes and hasattr(instance, attribute_name):
                    cls.from_json(
                        instance_name=attribute_name,
                        instance_owner=instance,
                        instance_json=json['instance'][attribute_name],
                        attachments_path=attachments_path,
                        excluded_attributes=excluded_attributes,
                        first_attributes=first_attributes
                    )


class BLBaseType:

    # exclude for all types
    # instance to json
    _common_excluded_attributes_get = ['bl_idname', 'original', 'rna_type', 'select']
    # json to instance
    _common_excluded_attributes_set = ['bis_linked_item', 'bl_idname', 'original', 'rna_type', 'select', 'type']
    # exclude for current type in child classes
    # json to instance
    excluded_attributes_get = []
    # json to instance
    excluded_attributes_set = []

    @classmethod
    def to_json(cls, instance):
        # instance to json call
        instance_in_json = {
            'class': instance.__class__.__name__,
            'instance': cls.instance_to_json(instance=instance)
        }
        return instance_in_json

    @classmethod
    def instance_to_json(cls, instance):
        # get data from instance and convert them to json
        return BlTypes.complex_to_json(
            instance=instance,
            excluded_attributes=cls.excluded_attr(aim='get')
        )

    @classmethod
    def from_json(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # instance from json call
        return cls.json_to_instance(
            instance_name=instance_name,
            instance_owner=instance_owner,
            json=json,
            attachments_path=attachments_path,
            excluded_attributes=excluded_attributes,
            first_attributes=first_attributes
            )

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # get data from json and fill instance with that data
        return BlTypes.complex_from_json(
            instance=getattr(instance_owner, instance_name),
            json=json,
            attachments_path=attachments_path,
            excluded_attributes=cls.excluded_attr(aim='set', additional_exclude=excluded_attributes),
            first_attributes=first_attributes
        )

    @classmethod
    def excluded_attr(cls, aim='get', additional_exclude: list = None):
        additional_exclude = additional_exclude if additional_exclude is not None else []
        if aim == 'get':
            return cls._common_excluded_attributes_get + cls.excluded_attributes_get + additional_exclude
        else:
            return cls._common_excluded_attributes_set + cls.excluded_attributes_set + additional_exclude


class BLbpy_prop_collection(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        json = []
        for key, item in instance.items():
            item_json = BlTypes.to_json(instance=item)
            json.append(item_json)
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # add new items if not exists
        instance = getattr(instance_owner, instance_name)
        items_exists = len(instance)
        if items_exists < len(json['instance']):
            for item_json in json['instance'][items_exists:]:
                item_class = None
                if hasattr(sys.modules[__name__], 'BL' + item_json['class']):
                    item_class = getattr(sys.modules[__name__], 'BL' + item_json['class'])
                if item_class and hasattr(item_class, 'new_item'):
                    item_class.new_item(item_owner=instance)
        # fill with data
        for i, item_json in enumerate(json['instance']):
            if i < len(instance):
                BlTypes.complex_from_json(
                    instance=instance[i],
                    json=item_json,
                    attachments_path=attachments_path,
                    excluded_attributes=excluded_attributes,
                    first_attributes=first_attributes
                )


class BLbpy_prop_array(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        json = []
        for item in instance:
            json.append(item)
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        instance = getattr(instance_owner, instance_name)
        for i, array_item_json in enumerate(json['instance']):
            instance[i] = array_item_json


# class BLNodeOutputFileSlotFile(BLBaseType):
#
#     @classmethod
#     def instance_to_json(cls, instance):
#         # data to json
#         json = {
#             'format': BLImageFormatSettings.to_json(instance.format),
#             'path': instance.path,
#             'use_node_format': instance.use_node_format
#         }
#         return json
#
#     @classmethod
#     def json_to_instance(cls, instance, json, instance_field=None):
#         # data from json
#         BLImageFormatSettings.from_json(instance.format, json['format'])
#         instance.path = json['path']
#         instance.use_node_format = json['use_node_format']
#         return instance
#
#     @classmethod
#     def new_item(cls, node):
#         # creates new real item
#         context_copy = bpy.context.copy()
#         context_copy['node'] = node
#         bpy.ops.node.output_file_add_socket(context_copy)


class BLColor(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {
            'r': instance.r,
            'g': instance.g,
            'b': instance.b
        }
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        instance = getattr(instance_owner, instance_name)
        instance.r = json['instance']['r']
        instance.g = json['instance']['g']
        instance.b = json['instance']['b']


class BLVector(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {
            'x': instance.x,
            'y': instance.y
        }
        if hasattr(instance, 'z'):
            json['z'] = instance.z
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        instance = getattr(instance_owner, instance_name)
        instance.x = json['instance']['x']
        instance.y = json['instance']['y']
        if hasattr(instance, 'z'):
            instance.z = json['instance']['z']


# class BLset:
#
#     @classmethod
#     def to_json(cls, instance):
#         # instance to json call
#         return list(instance)
#
#     @classmethod
#     def from_json(cls, json):
#         # instance from json call
#         return set(json)


class BLObject(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {}
        if instance:
            json['name'] = instance.name
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # data from json
        if 'name' in json['instance'] and json['instance']['name'] in bpy.data.objects:
            setattr(instance_owner, instance_name, bpy.data.objects[json['instance']['name']])


# class BLImage(BLBaseType):
#
#     excluded_attributes_get = ['pixels', 'filepath_raw']  # exclude for current type


class BLImage(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {}
        if instance:
            # json['source'] = instance.source
            json['filepath'] = os.path.normpath(os.path.join(os.path.dirname(bpy.data.filepath), instance.filepath.replace('//', '')))
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # data from json
        # all attachments (images) must be loaded first
        if 'filepath' in json['instance'] and json['instance']['filepath']:
            image_name = os.path.basename(json['instance']['filepath'])
            # find image file
            image_path = ''
            if os.path.exists(os.path.join(attachments_path, image_name)) and os.path.isfile(os.path.join(attachments_path, image_name)):
                # first look in received attachments
                image_path = os.path.join(attachments_path, image_name)
            elif os.path.exists(json['instance']['filepath']) and os.path.isfile(json['instance']['filepath']):
                # next look by original path
                image_path = json['instance']['filepath']
            # get image
            if image_path:
                image = bpy.data.images.load(image_path, check_existing=True)
                # image.source = json['instance']['source']
            elif image_name in bpy.data.images:
                image = bpy.data.images[image_name]
            else:
                image = None
            # set image as attribute
            if image:
                setattr(instance_owner, instance_name, image)


class BLText(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {}
        rez = TextManager.to_bis(context=bpy.context, text=instance)
        if rez['stat'] == 'OK':
            bis_linked_item = {
                'storage': TextManager.storage_type(),
                'id': rez['data']['id']
            }
            json['bis_linked_item'] = bis_linked_item
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # data from json
        rez = TextManager.from_bis(context=bpy.context, bis_text_id=json['instance']['bis_linked_item']['id'])
        if rez['stat'] == 'OK':
            text_item = TextManager.item_by_bis_uid(bis_uid=json['instance']['bis_linked_item']['id'])
            if text_item:
                setattr(instance_owner, instance_name, text_item)


class BLCurveMapping(BLBaseType):
    pass


class BLCurveMap(BLBaseType):
    pass


class BLCurveMapPoint(BLBaseType):

    @classmethod
    def new_item(cls, item_owner):
        # creates new item ot this type
        return item_owner.new(0.0, 0.0)


class BLColorRamp(BLBaseType):
    pass


class BLColorRampElement(BLBaseType):

    @classmethod
    def new_item(cls, item_owner):
        # creates new item ot this type
        return item_owner.new(0.0)


class BLTexture(BLBaseType):

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # data from json
        if 'name' in json['instance'] and 'type' in json['instance']:
            # create new anyway, because existed could be from other material
            new_item = bpy.data.textures.new(name=json['instance']['name'], type=json['instance']['type'])
            setattr(instance_owner, instance_name, new_item)
            BlTypes.complex_from_json(
                instance=new_item,
                json=json,
                attachments_path=attachments_path
            )


class BLBlendTexture(BLTexture):
    pass


class BLCloudsTexture(BLTexture):
    pass


class BLDistortedNoiseTexture(BLTexture):
    pass


# class BLImageTexture(BLTexture):
#     pass


class BLMagicTexture(BLTexture):
    pass


class BLMarbleTexture(BLTexture):
    pass


class BLMusgraveTexture(BLTexture):
    pass


class BLNoiseTexture(BLTexture):
    pass


class BLStucciTexture(BLTexture):
    pass


class BLVoronoiTexture(BLTexture):
    pass


class BLWoodTexture(BLTexture):
    pass


class BLScene(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {}
        if instance:
            json['name'] = instance.name
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # data from json
        if 'name' in json['instance'] and json['instance']['name'] in bpy.data.scenes:
            setattr(instance_owner, instance_name, bpy.data.scenes[json['instance']['name']])


class BLEuler(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {}
        if instance:
            json['order'] = instance.order
            json['x'] = instance.x
            json['y'] = instance.y
            json['z'] = instance.z
        return json

    @classmethod
    def json_to_instance(cls, instance_name, instance_owner, json, attachments_path=None, excluded_attributes: list = None, first_attributes: list = None):
        # data from json
        instance = getattr(instance_owner, instance_name)
        if hasattr(instance, 'order') and 'order' in json['instance'] and json['instance']['order']:
            instance.order = json['instance']['order']
        if hasattr(instance, 'x') and 'x' in json['instance']:
            instance.x = json['instance']['x']
        if hasattr(instance, 'y') and 'y' in json['instance']:
            instance.y = json['instance']['y']
        if hasattr(instance, 'z') and 'z' in json['instance']:
            instance.z = json['instance']['z']
        return instance


class BLNodeFrame(BLBaseType):

    @classmethod
    def instance_to_json(cls, instance):
        # data to json
        json = {
            'bis_node_uid': instance['bis_node_uid'] if 'bis_node_uid' in instance else None
        }
        return json


class BLNodeSocketFloat(BLBaseType):
    pass


class BLNodeSocketFloatFactor(BLBaseType):
    pass


class BLNodeSocketFloatUnsigned(BLBaseType):
    pass


class BLNodeSocketVector(BLBaseType):
    pass


class BLNodeSocketVectorEuler(BLBaseType):
    pass


class BLNodeSocketVectorTranslation(BLBaseType):
    pass


class BLNodeSocketVectorXYZ(BLBaseType):
    pass


class BLNodeSocketColor(BLBaseType):
    pass


class BLNodeSocketInt(BLBaseType):
    pass


class BLNodeSocketShader(BLBaseType):
    pass


class BLNodeSocketInterfaceFloat(BLBaseType):
    pass


class BLNodeSocketInterfaceFloatFactor(BLBaseType):
    pass


class BLNodeSocketInterfaceFloatUnsigned(BLBaseType):
    pass


class BLNodeSocketInterfaceInt(BLBaseType):
    pass


class BLNodeSocketInterfaceVector(BLBaseType):
    pass


class BLNodeSocketInterfaceVectorTranslation(BLBaseType):
    pass


class BLNodeSocketInterfaceVectorXYZ(BLBaseType):
    pass


class BLNodeSocketInterfaceColor(BLBaseType):
    pass


class BLNodeSocketInterfaceShader(BLBaseType):
    pass
