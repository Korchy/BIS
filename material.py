# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

# Material class for objects
import bpy
from .addon import Addon
from .node_tree import NodeTree
from .bl_types_conversion import BLbpy_prop_array


class Material:
    @classmethod
    def to_json(cls, context, material):
        # base material specification
        material_json = {
            'class': material.__class__.__name__,
            'instance': {
                'type': material.bl_rna.name,
                'name': material.name,
                'bl_type': material.node_tree.type,
                'render_engine': context.window.scene.render.engine,
                'diffuse_color': BLbpy_prop_array.to_json(material.diffuse_color),
                'metallic': material.metallic,
                'roughness': material.roughness,
                'bis_uid': material['bis_uid'] if 'bis_uid' in material else None,
                'node_tree': NodeTree.to_json(node_tree_parent=material, node_tree=material.node_tree)
            },
            'bis_version': Addon.current_version()
        }
        if hasattr(material, 'blend_method'):
            material_json['instance']['blend_method'] = material.blend_method
        if hasattr(material, 'shadow_method'):
            material_json['instance']['shadow_method'] = material.shadow_method
        # for current material specification
        cls._to_json_spec(material_json=material_json, material=material)
        return material_json

    @classmethod
    def _to_json_spec(cls, material_json, material):
        # extend to current material (different engines)
        pass

    @classmethod
    def from_json(cls, context,  material_json, material=None, attachments_path=''):
        if not material:
            material = cls.new(context=context)
            cls.clear(material=material)
        if material:
            # fill with data

            # TODO remove else condition after update to 1.9.0 - remain only inside if condition

            if 'bis_version' in material_json and material_json['bis_version'] == '1.9.0':
                material.name = material_json['instance']['name']
                if 'diffuse_color' in material_json and hasattr(material, 'diffuse_color'):
                    BLbpy_prop_array.from_json(material.diffuse_color, material_json['instance']['diffuse_color'])
                if 'metallic' in material_json and hasattr(material, 'metallic'):
                    material.metallic = material_json['instance']['metallic']
                if 'roughness' in material_json and hasattr(material, 'roughness'):
                    material.roughness = material_json['instance']['roughness']
                if 'blend_method' in material_json and hasattr(material, 'blend_method'):
                    material.blend_method = material_json['instance']['blend_method']
                if 'shadow_method' in material_json and hasattr(material, 'shadow_method'):
                    material.shadow_method = material_json['instance']['shadow_method']
                NodeTree.from_json(
                    node_tree_parent=material,
                    node_tree_json=material_json['instance']['node_tree'],
                    attachments_path=attachments_path,
                    bis_version=material_json['bis_version']
                )
                material['bis_uid'] = material_json['instance']['bis_uid'] if 'bis_uid' in material_json['instance'] else None
                material.name = material_json['instance']['name']  # to prevent .001 in name of new material if already exists some other materials with this name
            else:
                material.name = material_json['name']
                if 'diffuse_color' in material_json and hasattr(material, 'diffuse_color'):
                    BLbpy_prop_array.from_json(material.diffuse_color, material_json['diffuse_color'])
                if 'metallic' in material_json and hasattr(material, 'metallic'):
                    material.metallic = material_json['metallic']
                if 'roughness' in material_json and hasattr(material, 'roughness'):
                    material.roughness = material_json['roughness']
                if 'blend_method' in material_json and hasattr(material, 'blend_method'):
                    material.blend_method = material_json['blend_method']
                if 'shadow_method' in material_json and hasattr(material, 'shadow_method'):
                    material.shadow_method = material_json['shadow_method']
                NodeTree.from_json(node_tree_parent=material, node_tree_json=material_json['node_tree'], attachments_path=attachments_path)
                material['bis_uid'] = material_json['bis_uid'] if 'bis_uid' in material_json else None

            # for current material specification
            cls._from_json_spec(material=material, material_json=material_json, attachments_path=attachments_path)
        return material

    @classmethod
    def _from_json_spec(cls, material, material_json, attachments_path):
        # extend to current material (different engines)
        pass

    @classmethod
    def new(cls, context):
        # add new empty material
        material = None
        subtype = cls.get_subtype(context=context)
        if subtype == 'ShaderNodeTree':
            subtype2 = cls.get_subtype2(context=context)
            if subtype2 == 'WORLD':
                material = bpy.data.worlds.new(name='Material')
                material.use_nodes = True
                context.scene.world = material
            elif subtype2 == 'OBJECT':
                if context.active_object:
                    material = bpy.data.materials.new(name='Material')
                    material.use_nodes = True
                    context.active_object.active_material = material
        elif subtype == 'CompositorNodeTree':
            if not context.window.scene.use_nodes:
                context.window.scene.use_nodes = True
        return material

    @staticmethod
    def clear(material,  exclude_output_nodes=False):
        # clear material node tree
        NodeTree.clear(material.node_tree, exclude_output_nodes=exclude_output_nodes)

    @staticmethod
    def get_subtype(context):
        # return subtype
        if context.area and context.area.spaces.active.type == 'NODE_EDITOR':
            return context.area.spaces.active.tree_type
        else:
            return 'ShaderNodeTree'

    @staticmethod
    def get_subtype2(context):
        # return subtype2
        if context.area and context.area.spaces.active.type == 'NODE_EDITOR':
            return context.area.spaces.active.shader_type
        else:
            return 'OBJECT'
