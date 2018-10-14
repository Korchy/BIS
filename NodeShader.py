# Nikita Akimov
# interplanety@interplanety.org

import bpy
import os
from .JsonEx import JsonEx
from .NodeBase import NodeCommon, TMCommon, IUCommon, CMCommon, CurveMapping, NodeColorRamp
from .TextManager import TextManager


class NodeShaderNodeBsdfGlossy(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['distribution'] = node.distribution
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.distribution = node_in_json['distribution']
        return current_node


class NodeShaderNodeBsdfAnisotropic(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeBsdfGlass(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeBsdfRefraction(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeAttribute(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['attribute_name'] = node.attribute_name
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.attribute_name = node_in_json['attribute_name']
        return current_node


class NodeShaderNodeTangent(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['direction_type'] = node.direction_type
        node_json['axis'] = node.axis
        node_json['uv_map'] = node.uv_map
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.direction_type = node_in_json['direction_type']
        current_node.axis = node_in_json['axis']
        current_node.uv_map = node_in_json['uv_map']
        return current_node


class NodeShaderNodeUVMap(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['from_dupli'] = node.from_dupli
        node_json['uv_map'] = node.uv_map
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.from_dupli = node_in_json['from_dupli']
        current_node.uv_map = node_in_json['uv_map']
        return current_node


class NodeShaderNodeTexCoord(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['object'] = ''
        if node.object:
            node_json['object'] = node.object.name
        node_json['from_dupli'] = node.from_dupli
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        if node_in_json['object']:
            if node_in_json['object'] in bpy.data.objects:
                current_node.object = bpy.data.objects[node_in_json['object']]
        current_node.from_dupli = node_in_json['from_dupli']
        return current_node


class NodeShaderNodeTexPointDensity(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['object'] = ''
        node_json['particle_system'] = ''
        if node.object:
            node_json['object'] = node.object.name
            if node.particle_system:
                node_json['particle_system'] = node.particle_system.name
        node_json['point_source'] = node.point_source
        node_json['resolution'] = node.resolution
        node_json['radius'] = node.radius
        node_json['space'] = node.space
        node_json['interpolation'] = node.interpolation
        node_json['particle_color_source'] = node.particle_color_source
        node_json['vertex_color_source'] = node.vertex_color_source
        node_json['vertex_attribute_name'] = node.vertex_attribute_name
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        if node_in_json['object']:
            if node_in_json['object'] in bpy.data.objects:
                current_node.object = bpy.data.objects[node_in_json['object']]
                if node_in_json['particle_system']:
                    if node_in_json['particle_system'] in bpy.data.objects[node_in_json['object']].particle_systems:
                        current_node.particle_system = bpy.data.objects[node_in_json['object']].particle_systems[node_in_json['particle_system']]
        current_node.point_source = node_in_json['point_source']
        current_node.resolution = node_in_json['resolution']
        current_node.radius = node_in_json['radius']
        current_node.space = node_in_json['space']
        current_node.interpolation = node_in_json['interpolation']
        current_node.particle_color_source = node_in_json['particle_color_source']
        current_node.vertex_color_source = node_in_json['vertex_color_source']
        current_node.vertex_attribute_name = node_in_json['vertex_attribute_name']
        return current_node


class NodeShaderNodeTexEnvironment(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['image'] = ''
        node_json['image_source'] = ''
        if node.image:
            node_json['image'] = os.path.normpath(os.path.join(os.path.dirname(bpy.data.filepath), node.image.filepath.replace('//', '')))
            node_json['image_source'] = node.image.source
        node_json['color_space'] = node.color_space
        node_json['projection'] = node.projection
        node_json['interpolation'] = node.interpolation
        node_json['texture_mapping'] = TMCommon.tm_to_json(node.texture_mapping)
        node_json['image_user'] = IUCommon.iu_to_json(node.image_user)
        node_json['color_mapping'] = CMCommon.cm_to_json(node.color_mapping)
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        if node_in_json['image']:
            if os.path.exists(node_in_json['image']) and os.path.isfile(node_in_json['image']):
                if os.path.basename(node_in_json['image']) in bpy.data.images:
                    bpy.data.images[os.path.basename(node_in_json['image'])].reload()
                else:
                    bpy.data.images.load(node_in_json['image'], check_existing=True)
            if os.path.basename(node_in_json['image']) in bpy.data.images:
                current_node.image = bpy.data.images[os.path.basename(node_in_json['image'])]
                current_node.image.source = node_in_json['image_source']
        current_node.color_space = node_in_json['color_space']
        current_node.projection = node_in_json['projection']
        current_node.interpolation = node_in_json['interpolation']
        TMCommon.json_to_tm(current_node, node_in_json['texture_mapping'])
        IUCommon.json_to_iu(current_node, node_in_json['image_user'])
        CMCommon.json_to_cm(current_node, node_in_json['color_mapping'])
        return current_node


class NodeShaderNodeTexImage(NodeShaderNodeTexEnvironment):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['projection_blend'] = node.projection_blend
        node_json['extension'] = node.extension
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.projection_blend = node_in_json['projection_blend']
        current_node.extension = node_in_json['extension']
        return current_node


class NodeShaderNodeTexChecker(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['texture_mapping'] = TMCommon.tm_to_json(node.texture_mapping)
        node_json['color_mapping'] = CMCommon.cm_to_json(node.color_mapping)
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        TMCommon.json_to_tm(current_node, node_in_json['texture_mapping'])
        CMCommon.json_to_cm(current_node, node_in_json['color_mapping'])
        return current_node


class NodeShaderNodeTexBrick(NodeShaderNodeTexChecker):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['offset_frequency'] = node.offset_frequency
        node_json['squash_frequency'] = node.squash_frequency
        node_json['offset'] = node.offset
        node_json['squash'] = node.squash
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.offset_frequency = node_in_json['offset_frequency']
        current_node.squash_frequency = node_in_json['squash_frequency']
        current_node.offset = node_in_json['offset']
        current_node.squash = node_in_json['squash']
        return current_node


class NodeShaderNodeTexGradient(NodeShaderNodeTexChecker):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['gradient_type'] = node.gradient_type
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.gradient_type = node_in_json['gradient_type']
        return current_node


class NodeShaderNodeTexMagic(NodeShaderNodeTexChecker):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['turbulence_depth'] = node.turbulence_depth
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.turbulence_depth = node_in_json['turbulence_depth']
        return current_node


class NodeShaderNodeTexMusgrave(NodeShaderNodeTexChecker):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['musgrave_type'] = node.musgrave_type
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.musgrave_type = node_in_json['musgrave_type']
        return current_node


class NodeShaderNodeTexVoronoi(NodeShaderNodeTexChecker):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['coloring'] = node.coloring
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.coloring = node_in_json['coloring']
        return current_node


class NodeShaderNodeTexWave(NodeShaderNodeTexChecker):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['wave_type'] = node.wave_type
        node_json['wave_profile'] = node.wave_profile
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.wave_type = node_in_json['wave_type']
        current_node.wave_profile = node_in_json['wave_profile']
        return current_node


class NodeShaderNodeTexSky(NodeShaderNodeTexChecker):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['sky_type'] = node.sky_type
        node_json['sun_direction'] = JsonEx.vector3_to_json(node.sun_direction)
        node_json['turbidity'] = node.turbidity
        node_json['ground_albedo'] = node.ground_albedo
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.sky_type = node_in_json['sky_type']
        JsonEx.vector3_from_json(current_node.sun_direction, node_in_json['sun_direction'])
        current_node.turbidity = node_in_json['turbidity']
        current_node.ground_albedo = node_in_json['ground_albedo']
        return current_node


class NodeShaderNodeTexNoise(NodeShaderNodeTexChecker):
    pass


class NodeShaderNodeWireframe(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['use_pixel_size'] = node.use_pixel_size
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.use_pixel_size = node_in_json['use_pixel_size']
        return current_node


class NodeShaderNodeBsdfHair(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['component'] = node.component
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.component = node_in_json['component']
        return current_node


class NodeShaderNodeBsdfToon(NodeShaderNodeBsdfHair):
    pass


class NodeShaderNodeSubsurfaceScattering(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['falloff'] = node.falloff
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.falloff = node_in_json['falloff']
        return current_node


class NodeShaderNodeMixRGB(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['blend_type'] = node.blend_type
        node_json['use_alpha'] = node.use_alpha
        node_json['use_clamp'] = node.use_clamp
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.blend_type = node_in_json['blend_type']
        current_node.use_alpha = node_in_json['use_alpha']
        current_node.use_clamp = node_in_json['use_clamp']
        return current_node


class NodeShaderNodeBrightContrast(NodeCommon):
    pass


class NodeShaderNodeGamma(NodeCommon):
    pass


class NodeShaderNodeHueSaturation(NodeCommon):
    pass


class NodeShaderNodeInvert(NodeCommon):
    pass


class NodeShaderNodeLightFalloff(NodeCommon):
    pass


class NodeShaderNodeBlackbody(NodeCommon):
    pass


class NodeShaderNodeCombineHSV(NodeCommon):
    pass


class NodeShaderNodeSeparateHSV(NodeCommon):
    pass


class NodeShaderNodeCombineRGB(NodeCommon):
    pass


class NodeShaderNodeSeparateRGB(NodeCommon):
    pass


class NodeShaderNodeCombineXYZ(NodeCommon):
    pass


class NodeShaderNodeSeparateXYZ(NodeCommon):
    pass


class NodeShaderNodeRGBToBW(NodeCommon):
    pass


class NodeShaderNodeWavelength(NodeCommon):
    pass


class NodeShaderNodeRGBCurve(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['mapping'] = CurveMapping.cum_to_json(node.mapping)
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        CurveMapping.json_to_cum(current_node.mapping, node_in_json['mapping'])
        return current_node


class NodeShaderNodeVectorCurve(NodeShaderNodeRGBCurve):
    pass


class NodeShaderNodeBump(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['invert'] = node.invert
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.invert = node_in_json['invert']
        return current_node


class NodeShaderNodeVectorTransform(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['vector_type'] = node.vector_type
        node_json['convert_from'] = node.convert_from
        node_json['convert_to'] = node.convert_to
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.vector_type = node_in_json['vector_type']
        current_node.convert_from = node_in_json['convert_from']
        current_node.convert_to = node_in_json['convert_to']
        return current_node


class NodeShaderNodeValToRGB(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['color_ramp'] = NodeColorRamp.cr_to_json(node.color_ramp)
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        NodeColorRamp.json_to_cr(current_node.color_ramp, node_in_json['color_ramp'])
        return current_node


class NodeShaderNodeMapping(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['vector_type'] = node.vector_type
        node_json['translation'] = JsonEx.vector3_to_json(node.translation)
        node_json['rotation'] = JsonEx.vector3_to_json(node.rotation)
        node_json['scale'] = JsonEx.vector3_to_json(node.scale)
        node_json['min'] = JsonEx.vector3_to_json(node.min)
        node_json['max'] = JsonEx.vector3_to_json(node.max)
        node_json['use_min'] = node.use_min
        node_json['use_max'] = node.use_max
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.vector_type = node_in_json['vector_type']
        JsonEx.vector3_from_json(current_node.translation, node_in_json['translation'])
        JsonEx.vector3_from_json(current_node.rotation, node_in_json['rotation'])
        JsonEx.vector3_from_json(current_node.scale, node_in_json['scale'])
        JsonEx.vector3_from_json(current_node.min, node_in_json['min'])
        JsonEx.vector3_from_json(current_node.max, node_in_json['max'])
        current_node.use_min = node_in_json['use_min']
        current_node.use_max = node_in_json['use_max']
        return current_node


class NodeShaderNodeMath(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['operation'] = node.operation
        node_json['use_clamp'] = node.use_clamp
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.operation = node_in_json['operation']
        current_node.use_clamp = node_in_json['use_clamp']
        return current_node


class NodeShaderNodeVectorMath(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['operation'] = node.operation
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.operation = node_in_json['operation']
        return current_node


class NodeShaderNodeScript(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['script'] = ''
        node_json['script_bis_id'] = None
        if node.script:
            node_json['script'] = node.script.name
            rez = TextManager.toBis(bpy.context, bpy.data.texts[node.script.name])
            node_json['script_bis_id'] = ''
            if rez['stat'] == 'OK':
                node_json['script_bis_id'] = rez['data']['id']
        node_json['filepath'] = ''
        if node.filepath:
            if node.filepath[:2] == '//':
                node_json['filepath'] = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), node.filepath[2:]))
            else:
                node_json['filepath'] = os.path.abspath(node.filepath)
        node_json['mode'] = node.mode
        node_json['use_auto_update'] = node.use_auto_update
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.mode = node_in_json['mode']
        if node_in_json['script_bis_id']:
            TextManager.fromBis(bpy.context, node_in_json['script_bis_id'])
        if node_in_json['script']:
            if node_in_json['script'] in bpy.data.texts:
                current_node.script = bpy.data.texts[node_in_json['script']]
        if node_in_json['filepath']:
            if os.path.exists(node_in_json['filepath']) and os.path.isfile(node_in_json['filepath']):
                current_node.filepath = node_in_json['filepath']
        current_node.use_auto_update = node_in_json['use_auto_update']
        current_node.update()
        return current_node


class NodeNodeGroupInput(NodeCommon):
    pass


class NodeNodeGroupOutput(NodeCommon):
    @staticmethod
    def node_to_json(node):
        node_json = super(__class__, __class__).node_to_json(node)
        node_json['is_active_output'] = node.is_active_output
        return node_json

    @staticmethod
    def json_to_node(node_tree, node_in_json):
        current_node = super(__class__, __class__).json_to_node(node_tree, node_in_json)
        current_node.is_active_output = node_in_json['is_active_output']
        return current_node
