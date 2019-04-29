# Nikita Akimov
# interplanety@interplanety.org

# Material class for objects
import bpy
from .node_tree import NodeTree
from .bl_types_conversion import BLbpy_prop_array


class Material:
    @classmethod
    def to_json(cls, context, material):
        # base material specification
        material_json = {
            'type': material.bl_rna.name,
            'name': material.name,
            'bl_type': material.node_tree.type,
            'render_engine': context.window.scene.render.engine,
            'diffuse_color': BLbpy_prop_array.to_json(material.diffuse_color),
            'metallic': material.metallic,
            'roughness': material.roughness,
            'bis_uid': material['bis_uid'] if 'bis_uid' in material else None,
            'node_tree': NodeTree.to_json(material.node_tree)
        }
        # for current material specification
        cls._to_json_spec(material_json=material_json, material=material)
        return material_json

    @classmethod
    def _to_json_spec(cls, material_json, material):
        # extend to current material (different engines)
        pass

    @classmethod
    def from_json(cls, context, material_json):
        material = __class__.new(context=context)
        if material:
            # fill with data
            BLbpy_prop_array.from_json(material.diffuse_color, material_json['diffuse_color'])
            material.metallic = material_json['metallic']
            material.roughness = material_json['roughness']
            material['bis_uid'] = material_json['bis_uid'] if 'bis_uid' in material_json else None
            NodeTree.from_json(node_tree_parent=material, node_tree_json=material_json['node_tree'])
            # for current material specification
            cls._from_json_spec(material, material_json)
        return material

    @classmethod
    def _from_json_spec(cls, material, material_json):
        # extend to current material (different engines)
        pass

    @staticmethod
    def new(context):
        # add new empty material
        material = None
        subtype = __class__.get_subtype(context=context)
        if subtype == 'ShaderNodeTree':
            if context.active_object:
                material = bpy.data.materials.new(name='Material')
                material.use_nodes = True
                NodeTree.clear(material.node_tree)
                context.active_object.active_material = material
        elif subtype == 'CompositorNodeTree':
            if not context.window.scene.use_nodes:
                context.window.scene.use_nodes = True
        return material

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
