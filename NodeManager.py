# Nikita Akimov
# interplanety@interplanety.org

import sys
import bpy
import os
from . import JsonEx
from . import TextManager


class NodeManager():

    @staticmethod
    def nodeGroupToJson(nodeGroup):
        groupInJson = None
        if nodeGroup.type == 'GROUP':
            groupInJson = NodeShaderNodeGroup.nodeToJson(nodeGroup)
            # Write to file
            # import os
            # import json
            # with open(os.path.dirname(bpy.data.filepath) + os.sep + 'GroupNode.json', 'w') as currentFile:
            #     json.dump(groupInJson, currentFile, indent = 4)
        return groupInJson

    @staticmethod
    def jsonToNodeGroup(destNodeTree, nodeInJson):
        currentNode = None
        if destNodeTree:
            nodeClass = NodeCommon
            if hasattr(sys.modules[__name__], 'Node' + nodeInJson['bl_type']):
                nodeClass = getattr(sys.modules[__name__], 'Node' + nodeInJson['bl_type'])
            currentNode = nodeClass.jsonToNode(nodeTree=destNodeTree, nodeInJson=nodeInJson)
            currentNode.location = (0, 0)
        return currentNode


# Node
class NodeCommon():
    @staticmethod
    def nodeToJson(node):
        jsonEx = JsonEx.JsonEx
        return {
            'type': node.type,
            'tree_type': bpy.context.area.spaces.active.tree_type,
            'bl_type': node.bl_idname,
            'name': node.name,
            'label': node.label,
            'hide': node.hide,
            'location': jsonEx.vector2ToJson(node.location),
            'width': node.width,
            'height': node.height,
            'use_custom_color': node.use_custom_color,
            'color': jsonEx.colorToJson(node.color),
            'inputs': [],
            'outputs': []
        }
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        jsonEx = JsonEx.JsonEx
        currentNode = nodeTree.nodes.new(type = nodeInJson['bl_type'])
        currentNode.name = nodeInJson['name']
        currentNode.hide = nodeInJson['hide']
        currentNode.label = nodeInJson['label']
        jsonEx.vector2LoadFromJson(currentNode.location, nodeInJson['location'])
        currentNode.width = nodeInJson['width']
        currentNode.height = nodeInJson['height']
        currentNode.use_custom_color = nodeInJson['use_custom_color']
        jsonEx.colorLoadFromJson(currentNode.color, nodeInJson['color'])
        return currentNode


class NodeShaderNodeBsdfGlossy(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['distribution'] = node.distribution
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.distribution = nodeInJson['distribution']
        return currentNode


class NodeShaderNodeBsdfAnisotropic(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeBsdfGlass(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeBsdfRefraction(NodeShaderNodeBsdfGlossy):
    pass


class NodeShaderNodeAttribute(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['attribute_name'] = node.attribute_name
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.attribute_name = nodeInJson['attribute_name']
        return currentNode


class NodeShaderNodeTangent(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['direction_type'] = node.direction_type
        nodeJson['axis'] = node.axis
        nodeJson['uv_map'] = node.uv_map
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.direction_type = nodeInJson['direction_type']
        currentNode.axis = nodeInJson['axis']
        currentNode.uv_map = nodeInJson['uv_map']
        return currentNode


class NodeShaderNodeUVMap(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['from_dupli'] = node.from_dupli
        nodeJson['uv_map'] = node.uv_map
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.from_dupli = nodeInJson['from_dupli']
        currentNode.uv_map = nodeInJson['uv_map']
        return currentNode


class NodeShaderNodeTexCoord(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['object'] = ''
        if node.object:
            nodeJson['object'] = node.object.name
        nodeJson['from_dupli'] = node.from_dupli
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        if nodeInJson['object']:
            if nodeInJson['object'] in bpy.data.objects:
                currentNode.object = bpy.data.objects[nodeInJson['object']]
        currentNode.from_dupli = nodeInJson['from_dupli']
        return currentNode


class NodeShaderNodeTexPointDensity(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['object'] = ''
        nodeJson['particle_system'] = ''
        if node.object:
            nodeJson['object'] = node.object.name
            if node.particle_system:
                nodeJson['particle_system'] = node.particle_system.name
        nodeJson['point_source'] = node.point_source
        nodeJson['resolution'] = node.resolution
        nodeJson['radius'] = node.radius
        nodeJson['space'] = node.space
        nodeJson['interpolation'] = node.interpolation
        nodeJson['particle_color_source'] = node.particle_color_source
        nodeJson['vertex_color_source'] = node.vertex_color_source
        nodeJson['vertex_attribute_name'] = node.vertex_attribute_name
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        if nodeInJson['object']:
            if nodeInJson['object'] in bpy.data.objects:
                currentNode.object = bpy.data.objects[nodeInJson['object']]
                if nodeInJson['particle_system']:
                    if nodeInJson['particle_system'] in bpy.data.objects[nodeInJson['object']].particle_systems:
                        currentNode.particle_system = bpy.data.objects[nodeInJson['object']].particle_systems[nodeInJson['particle_system']]
        currentNode.point_source = nodeInJson['point_source']
        currentNode.resolution = nodeInJson['resolution']
        currentNode.radius = nodeInJson['radius']
        currentNode.space = nodeInJson['space']
        currentNode.interpolation = nodeInJson['interpolation']
        currentNode.particle_color_source = nodeInJson['particle_color_source']
        currentNode.vertex_color_source = nodeInJson['vertex_color_source']
        currentNode.vertex_attribute_name = nodeInJson['vertex_attribute_name']
        return currentNode


class NodeShaderNodeTexEnvironment(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['image'] = ''
        nodeJson['image_source'] = ''
        if node.image:
            nodeJson['image'] = node.image.filepath
            nodeJson['image_source'] = node.image.source
        nodeJson['color_space'] = node.color_space
        nodeJson['projection'] = node.projection
        nodeJson['interpolation'] = node.interpolation
        nodeJson['texture_mapping'] = TMCommon.tmToJson(node.texture_mapping)
        nodeJson['image_user'] = IUCommon.iuToJson(node.image_user)
        nodeJson['color_mapping'] = CMCommon.cmToJson(node.color_mapping)
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        if nodeInJson['image']:
            if os.path.exists(nodeInJson['image']) and os.path.isfile(nodeInJson['image']):
                if os.path.basename(nodeInJson['image']) in bpy.data.images:
                    bpy.data.images[os.path.basename(nodeInJson['image'])].reload()
                else:
                    bpy.data.images.load(nodeInJson['image'], check_existing = True)
            if os.path.basename(nodeInJson['image']) in bpy.data.images:
                currentNode.image = bpy.data.images[os.path.basename(nodeInJson['image'])]
                currentNode.image.source = nodeInJson['image_source']
        currentNode.color_space = nodeInJson['color_space']
        currentNode.projection = nodeInJson['projection']
        currentNode.interpolation = nodeInJson['interpolation']
        TMCommon.jsonToTm(currentNode, nodeInJson['texture_mapping'])
        IUCommon.jsonToIu(currentNode, nodeInJson['image_user'])
        CMCommon.jsonToCm(currentNode, nodeInJson['color_mapping'])
        return currentNode


class NodeShaderNodeTexImage(NodeShaderNodeTexEnvironment):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['projection_blend'] = node.projection_blend
        nodeJson['extension'] = node.extension
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.projection_blend = nodeInJson['projection_blend']
        currentNode.extension = nodeInJson['extension']
        return currentNode


class NodeShaderNodeTexChecker(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['texture_mapping'] = TMCommon.tmToJson(node.texture_mapping)
        nodeJson['color_mapping'] = CMCommon.cmToJson(node.color_mapping)
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        TMCommon.jsonToTm(currentNode, nodeInJson['texture_mapping'])
        CMCommon.jsonToCm(currentNode, nodeInJson['color_mapping'])
        return currentNode


class NodeShaderNodeTexBrick(NodeShaderNodeTexChecker):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['offset_frequency'] = node.offset_frequency
        nodeJson['squash_frequency'] = node.squash_frequency
        nodeJson['offset'] = node.offset
        nodeJson['squash'] = node.squash
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.offset_frequency = nodeInJson['offset_frequency']
        currentNode.squash_frequency = nodeInJson['squash_frequency']
        currentNode.offset = nodeInJson['offset']
        currentNode.squash = nodeInJson['squash']
        return currentNode


class NodeShaderNodeTexGradient(NodeShaderNodeTexChecker):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['gradient_type'] = node.gradient_type
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.gradient_type = nodeInJson['gradient_type']
        return currentNode


class NodeShaderNodeTexMagic(NodeShaderNodeTexChecker):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['turbulence_depth'] = node.turbulence_depth
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.turbulence_depth = nodeInJson['turbulence_depth']
        return currentNode


class NodeShaderNodeTexMusgrave(NodeShaderNodeTexChecker):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['musgrave_type'] = node.musgrave_type
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.musgrave_type = nodeInJson['musgrave_type']
        return currentNode


class NodeShaderNodeTexVoronoi(NodeShaderNodeTexChecker):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['coloring'] = node.coloring
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.coloring = nodeInJson['coloring']
        return currentNode


class NodeShaderNodeTexWave(NodeShaderNodeTexChecker):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['wave_type'] = node.wave_type
        nodeJson['wave_profile'] = node.wave_profile
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.wave_type = nodeInJson['wave_type']
        currentNode.wave_profile = nodeInJson['wave_profile']
        return currentNode


class NodeShaderNodeTexSky(NodeShaderNodeTexChecker):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        jsonEx = JsonEx.JsonEx
        nodeJson['sky_type'] = node.sky_type
        nodeJson['sun_direction'] = jsonEx.vector3ToJson(node.sun_direction)
        nodeJson['turbidity'] = node.turbidity
        nodeJson['ground_albedo'] = node.ground_albedo
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        jsonEx = JsonEx.JsonEx
        currentNode.sky_type = nodeInJson['sky_type']
        jsonEx.vector3LoadFromJson(currentNode.sun_direction, nodeInJson['sun_direction'])
        currentNode.turbidity = nodeInJson['turbidity']
        currentNode.ground_albedo = nodeInJson['ground_albedo']
        return currentNode


class NodeShaderNodeTexNoise(NodeShaderNodeTexChecker):
    pass


class NodeShaderNodeWireframe(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['use_pixel_size'] = node.use_pixel_size
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.use_pixel_size = nodeInJson['use_pixel_size']
        return currentNode


class NodeShaderNodeBsdfHair(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['component'] = node.component
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.component = nodeInJson['component']
        return currentNode


class NodeShaderNodeBsdfToon(NodeShaderNodeBsdfHair):
    pass


class NodeShaderNodeSubsurfaceScattering(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['falloff'] = node.falloff
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.falloff = nodeInJson['falloff']
        return currentNode


class NodeShaderNodeMixRGB(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['blend_type'] = node.blend_type
        nodeJson['use_alpha'] = node.use_alpha
        nodeJson['use_clamp'] = node.use_clamp
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.blend_type = nodeInJson['blend_type']
        currentNode.use_alpha = nodeInJson['use_alpha']
        currentNode.use_clamp = nodeInJson['use_clamp']
        return currentNode


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
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['mapping'] = CurveMapping.cumToJson(node.mapping)
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        CurveMapping.jsonToCum(currentNode.mapping, nodeInJson['mapping'])
        return currentNode


class NodeShaderNodeVectorCurve(NodeShaderNodeRGBCurve):
    pass


class NodeShaderNodeBump(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['invert'] = node.invert
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.invert = nodeInJson['invert']
        return currentNode


class NodeShaderNodeVectorTransform(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['vector_type'] = node.vector_type
        nodeJson['convert_from'] = node.convert_from
        nodeJson['convert_to'] = node.convert_to
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.vector_type = nodeInJson['vector_type']
        currentNode.convert_from = nodeInJson['convert_from']
        currentNode.convert_to = nodeInJson['convert_to']
        return currentNode


class NodeShaderNodeValToRGB(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['color_ramp'] = NodeColorRamp.crToJson(node.color_ramp)
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        NodeColorRamp.jsonToCr(currentNode.color_ramp, nodeInJson['color_ramp'])
        return currentNode


class NodeShaderNodeMapping(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        jsonEx = JsonEx.JsonEx
        nodeJson['vector_type'] = node.vector_type
        nodeJson['translation'] = jsonEx.vector3ToJson(node.translation)
        nodeJson['rotation'] = jsonEx.vector3ToJson(node.rotation)
        nodeJson['scale'] = jsonEx.vector3ToJson(node.scale)
        nodeJson['min'] = jsonEx.vector3ToJson(node.min)
        nodeJson['max'] = jsonEx.vector3ToJson(node.max)
        nodeJson['use_min'] = node.use_min
        nodeJson['use_max'] = node.use_max
        return nodeJson

    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        jsonEx = JsonEx.JsonEx
        currentNode.vector_type = nodeInJson['vector_type']
        jsonEx.vector3LoadFromJson(currentNode.translation, nodeInJson['translation'])
        jsonEx.vector3LoadFromJson(currentNode.rotation, nodeInJson['rotation'])
        jsonEx.vector3LoadFromJson(currentNode.scale, nodeInJson['scale'])
        jsonEx.vector3LoadFromJson(currentNode.min, nodeInJson['min'])
        jsonEx.vector3LoadFromJson(currentNode.max, nodeInJson['max'])
        currentNode.use_min = nodeInJson['use_min']
        currentNode.use_max = nodeInJson['use_max']
        return currentNode


class NodeShaderNodeMath(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['operation'] = node.operation
        nodeJson['use_clamp'] = node.use_clamp
        return nodeJson

    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.operation = nodeInJson['operation']
        currentNode.use_clamp = nodeInJson['use_clamp']
        return currentNode


class NodeShaderNodeVectorMath(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['operation'] = node.operation
        return nodeJson

    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.operation = nodeInJson['operation']
        return currentNode


class NodeShaderNodeScript(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['script'] = ''
        nodeJson['script_bis_id'] = None
        if node.script:
            nodeJson['script'] = node.script.name
            rez = TextManager.TextManager.toBis(bpy.data.texts[node.script.name])
            nodeJson['script_bis_id'] = ''
            if rez['stat'] == 'OK':
                nodeJson['script_bis_id'] = rez['data']['id']
        nodeJson['filepath'] = ''
        if node.filepath:
            if node.filepath[:2] == '//':
                nodeJson['filepath'] = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), node.filepath[2:]))
            else:
                nodeJson['filepath'] = os.path.abspath(node.filepath)
        nodeJson['mode'] = node.mode
        nodeJson['use_auto_update'] = node.use_auto_update
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        currentNode.mode = nodeInJson['mode']
        if nodeInJson['script_bis_id']:
            TextManager.TextManager.fromBis(nodeInJson['script_bis_id'])
        if nodeInJson['script']:
            if nodeInJson['script'] in bpy.data.texts:
                currentNode.script = bpy.data.texts[nodeInJson['script']]
        if nodeInJson['filepath']:
            if os.path.exists(nodeInJson['filepath']) and os.path.isfile(nodeInJson['filepath']):
                currentNode.filepath = nodeInJson['filepath']
        currentNode.use_auto_update = nodeInJson['use_auto_update']
        currentNode.update()
        return currentNode


class NodeShaderNodeGroup(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(__class__, __class__).nodeToJson(node)
        nodeJson['nodes'] = []
        nodeJson['links'] = []
        nodeJson['GroupInput'] = []
        nodeJson['GroupOutput'] = []
        nodeGroupTree = node.node_tree
        nodeJson['name'] = nodeGroupTree.name
        # indexing
        nodeGroupTreeNodes = nodeGroupTree.nodes
        nodeGroupTreeNodesIndexed = []
        for currentNode in nodeGroupTreeNodes:
            inputs = []
            for input in currentNode.inputs:
                inputs.append(input)
            outputs = []
            for output in currentNode.outputs:
                outputs.append(output)
            nodeGroupTreeNodesIndexed.append([currentNode, inputs, outputs])
        # Nodes
        for currentNode in nodeGroupTreeNodesIndexed:
            nodeClass = NodeCommon
            if hasattr(sys.modules[__name__], 'Node' + currentNode[0].bl_idname):
                nodeClass = getattr(sys.modules[__name__], 'Node' + currentNode[0].bl_idname)
            currentNodeJson = nodeClass.nodeToJson(currentNode[0])
            for input in currentNode[1]:
                ioName = 'IO' + input.bl_idname
                if currentNode[0].bl_idname == 'NodeGroupInput' or currentNode[0].bl_idname == 'NodeGroupOutput':
                    ioName = 'IO' + currentNode[0].bl_idname
                ioClass = IOCommon
                if hasattr(sys.modules[__name__], ioName):
                    ioClass = getattr(sys.modules[__name__], ioName)
                    currentNodeJson['inputs'].append(ioClass.ioToJson(input))
            for output in currentNode[2]:
                ioName = 'IO' + output.bl_idname
                if currentNode[0].bl_idname == 'NodeGroupInput' or currentNode[0].bl_idname == 'NodeGroupOutput':
                    ioName = 'IO' + currentNode[0].bl_idname
                ioClass = IOCommon
                if hasattr(sys.modules[__name__], ioName):
                    ioClass = getattr(sys.modules[__name__], ioName)
                    currentNodeJson['outputs'].append(ioClass.ioToJson(output))
            nodeJson['nodes'].append(currentNodeJson)
        # GroupInputs
        for i, input in enumerate(nodeGroupTree.inputs):
            gioClass = GIOCommon
            if hasattr(sys.modules[__name__], 'GIO' + input.bl_socket_idname):
                gioClass = getattr(sys.modules[__name__], 'GIO' + input.bl_socket_idname)
            nodeJson['GroupInput'].append(gioClass.gioToJson(input, node.inputs[i]))
        # GroupOutputs
        for output in nodeGroupTree.outputs:
            gioClass = GIOCommon
            if hasattr(sys.modules[__name__], 'GIO' + output.bl_socket_idname):
                gioClass = getattr(sys.modules[__name__], 'GIO' + output.bl_socket_idname)
            nodeJson['GroupOutput'].append(gioClass.gioToJson(output))
        # Links
        for link in nodeGroupTree.links:
            fromNodeIndex = 0
            fromNodeOutputIndex = 0
            toNodeIndex = 0
            toNodeInputIndex = 0
            nodeIndex = 0
            for nodeData in nodeGroupTreeNodesIndexed:
                if link.from_node in nodeData:
                    fromNodeIndex = nodeIndex
                    if link.from_socket in nodeData[2]:
                        fromNodeOutputIndex = nodeData[2].index(link.from_socket)
                if link.to_node in nodeData:
                    toNodeIndex = nodeIndex
                    if link.to_socket in nodeData[1]:
                        toNodeInputIndex = nodeData[1].index(link.to_socket)
                nodeIndex += 1
            nodeJson['links'].append([fromNodeIndex, fromNodeOutputIndex, toNodeIndex, toNodeInputIndex])
        return nodeJson
    @staticmethod
    def jsonToNode(nodeTree, nodeInJson):
        currentNode = super(__class__, __class__).jsonToNode(nodeTree, nodeInJson)
        tree_type = nodeInJson['tree_type'] if 'tree_type' in nodeInJson else bpy.context.area.spaces.active.tree_type
        currentNode.node_tree = bpy.data.node_groups.new(type=tree_type, name=nodeInJson['name'])
        nodeGroupTreeNodesIndexed = []
        # GroupInputs
        for i, inputInJson in enumerate(nodeInJson['GroupInput']):
            gioClass = GIOCommon
            if hasattr(sys.modules[__name__], 'GIO' + inputInJson['bl_type']):
                gioClass = getattr(sys.modules[__name__], 'GIO' + inputInJson['bl_type'])
            gioClass.jsonToGi(nodeTree=currentNode.node_tree,
                              groupNode=currentNode,
                              inputNumber=i,
                              inputInJson=inputInJson)
        # GroupOutputs
        for outputInJson in nodeInJson['GroupOutput']:
            gioClass = GIOCommon
            if hasattr(sys.modules[__name__], 'GIO' + outputInJson['bl_type']):
                gioClass = getattr(sys.modules[__name__], 'GIO' + outputInJson['bl_type'])
            gioClass.jsonToGo(nodeTree=currentNode.node_tree,
                              outputInJson=outputInJson)
        # Nodes
        for currentNodeInJson in nodeInJson['nodes']:
            cNode = None
            nodeClass = NodeCommon
            if hasattr(sys.modules[__name__], 'Node' + currentNodeInJson['bl_type']):
                nodeClass = getattr(sys.modules[__name__], 'Node' + currentNodeInJson['bl_type'])
            cNode = nodeClass.jsonToNode(nodeTree = currentNode.node_tree,
                                               nodeInJson = currentNodeInJson)
            if cNode:
                # Node Inputs
                currentInputs = []
                for inputNumber, nodeInputInJson in enumerate(currentNodeInJson['inputs']):
                    if len(cNode.inputs) > inputNumber:
                        if nodeInputInJson:
                            ioClass = IOCommon
                            if hasattr(sys.modules[__name__], 'IO' + nodeInputInJson['bl_type']):
                                ioClass = getattr(sys.modules[__name__], 'IO' + nodeInputInJson['bl_type'])
                            if __class__.ioTypesCompatibility(cNode.inputs[inputNumber].bl_idname, nodeInputInJson['bl_type']):
                                ioClass.jsonToI(node = cNode,
                                                inputNumber = inputNumber,
                                                inputInJson = nodeInputInJson)
                        currentInputs.append(cNode.inputs[inputNumber])
                # Node Outputs
                currentOutputs = []
                for outputNumber, nodeOutputInJson in enumerate(currentNodeInJson['outputs']):
                    if len(cNode.outputs) > outputNumber:
                        if nodeOutputInJson:
                            ioClass = IOCommon
                            if hasattr(sys.modules[__name__], 'IO' + nodeOutputInJson['bl_type']):
                                ioClass = getattr(sys.modules[__name__], 'IO' + nodeOutputInJson['bl_type'])
                            if __class__.ioTypesCompatibility(cNode.outputs[outputNumber].bl_idname, nodeOutputInJson['bl_type']):
                                ioClass.jsonToO(node = cNode,
                                                outputNumber = outputNumber,
                                                outputInJson = nodeOutputInJson)
                        currentOutputs.append(cNode.outputs[outputNumber])
                nodeGroupTreeNodesIndexed.append([currentInputs, currentOutputs])
        # Links
        for linkInJson in nodeInJson['links']:
            if linkInJson[1] in range(len(nodeGroupTreeNodesIndexed[linkInJson[0]][1])) and linkInJson[3] in range(len(nodeGroupTreeNodesIndexed[linkInJson[2]][0])):
                fromOutput = nodeGroupTreeNodesIndexed[linkInJson[0]][1][linkInJson[1]]
                toInput = nodeGroupTreeNodesIndexed[linkInJson[2]][0][linkInJson[3]]
                currentNode.node_tree.links.new(fromOutput, toInput)
        return currentNode
    @staticmethod
    def ioTypesCompatibility(ioType1, ioType2):
        # for older compatibilty SocketFloatFactor = SocketFloat (ex: MixRGB)
        compatible = ['NodeSocketFloat', 'NodeSocketFloatFactor']
        if ioType1 == ioType2 or (ioType1 in compatible and ioType2 in compatible):
            return True


# Node TextureMapping
class TMCommon():
    @staticmethod
    def tmToJson(tm):
        jsonEx = JsonEx.JsonEx
        return {
            'vector_type': tm.vector_type,
            'translation': jsonEx.vector3ToJson(tm.translation),
            'rotation': jsonEx.vector3ToJson(tm.rotation),
            'scale': jsonEx.vector3ToJson(tm.scale),
            'min': jsonEx.vector3ToJson(tm.min),
            'max': jsonEx.vector3ToJson(tm.max),
            'use_min': tm.use_min,
            'use_max': tm.use_max,
            'mapping_x': tm.mapping_x,
            'mapping_y': tm.mapping_y,
            'mapping_z': tm.mapping_z,
            'mapping': tm.mapping
        }
    @staticmethod
    def jsonToTm(node, tmInJson):
        jsonEx = JsonEx.JsonEx
        node.texture_mapping.vector_type = tmInJson['vector_type']
        jsonEx.vector3LoadFromJson(node.texture_mapping.translation, tmInJson['translation'])
        jsonEx.vector3LoadFromJson(node.texture_mapping.rotation, tmInJson['rotation'])
        jsonEx.vector3LoadFromJson(node.texture_mapping.scale, tmInJson['scale'])
        jsonEx.vector3LoadFromJson(node.texture_mapping.min, tmInJson['min'])
        jsonEx.vector3LoadFromJson(node.texture_mapping.max, tmInJson['max'])
        node.texture_mapping.use_min = tmInJson['use_min']
        node.texture_mapping.use_max = tmInJson['use_max']
        node.texture_mapping.mapping_x = tmInJson['mapping_x']
        node.texture_mapping.mapping_y = tmInJson['mapping_y']
        node.texture_mapping.mapping_z = tmInJson['mapping_z']
        node.texture_mapping.mapping = tmInJson['mapping']


# Node ImageUser
class IUCommon():
    @staticmethod
    def iuToJson(iu):
        return {
            'use_auto_refresh': iu.use_auto_refresh,
            'frame_current': iu.frame_current,
            'use_cyclic': iu.use_cyclic,
            'frame_duration': iu.frame_duration,
            'frame_offset': iu.frame_offset,
            'frame_start': iu.frame_start,
            'fields_per_frame': iu.fields_per_frame
        }
    @staticmethod
    def jsonToIu(node, iuInJson):
        node.image_user.use_auto_refresh = iuInJson['use_auto_refresh']
        node.image_user.frame_current = iuInJson['frame_current']
        node.image_user.use_cyclic = iuInJson['use_cyclic']
        node.image_user.frame_duration = iuInJson['frame_duration']
        node.image_user.frame_offset = iuInJson['frame_offset']
        node.image_user.frame_start = iuInJson['frame_start']
        node.image_user.fields_per_frame = iuInJson['fields_per_frame']


# Node ColorMapping
class CMCommon():
    @staticmethod
    def cmToJson(cm):
        jsonEx = JsonEx.JsonEx
        return {
            'use_color_ramp': cm.use_color_ramp,
            'brightness': cm.brightness,
            'contrast': cm.contrast,
            'saturation': cm.saturation,
            'blend_type': cm.blend_type,
            'blend_color': jsonEx.colorToJson(cm.blend_color),
            'blend_factor': cm.blend_factor,
            'color_ramp': NodeColorRamp.crToJson(cm.color_ramp)
        }
    @staticmethod
    def jsonToCm(node, cmInJson):
        jsonEx = JsonEx.JsonEx
        node.color_mapping.use_color_ramp = cmInJson['use_color_ramp']
        node.color_mapping.brightness = cmInJson['brightness']
        node.color_mapping.contrast = cmInJson['contrast']
        node.color_mapping.saturation = cmInJson['saturation']
        node.color_mapping.blend_type = cmInJson['blend_type']
        jsonEx.colorLoadFromJson(node.color_mapping.blend_color, cmInJson['blend_color'])
        node.color_mapping.blend_factor = cmInJson['blend_factor']
        NodeColorRamp.jsonToCr(node.color_mapping.color_ramp, cmInJson['color_ramp'])


# Node ColorRamp
class NodeColorRamp():
    @staticmethod
    def crToJson(cr):
        rez = {
            'interpolation': cr.interpolation,
            'hue_interpolation': cr.hue_interpolation,
            'color_mode': cr.color_mode,
            'elements': []
        }
        jsonEx = JsonEx.JsonEx
        for element in cr.elements:
            rez['elements'].append({
                'color': jsonEx.propArrayToJson(element.color),
                'alpha': element.alpha,
                'position': element.position
            })
        return rez
    @staticmethod
    def jsonToCr(colorRamp, crInJson):
        colorRamp.interpolation = crInJson['interpolation']
        colorRamp.hue_interpolation = crInJson['hue_interpolation']
        colorRamp.color_mode = crInJson['color_mode']
        jsonEx = JsonEx.JsonEx
        for i, element in enumerate(crInJson['elements']):
            if len(colorRamp.elements) <= i:
                colorRamp.elements.new(element['position'])
            colorRamp.elements[i].position = element['position']
            colorRamp.elements[i].alpha = element['alpha']
            jsonEx.propArrayLoadFromJson(colorRamp.elements[i].color, element['color'])


# Node Curve Mapping (mapping)
class CurveMapping():
    @staticmethod
    def cumToJson(cum):
        jsonEx = JsonEx.JsonEx
        rez = {
            'use_clip': cum.use_clip,
            'clip_min_x': cum.clip_min_x,
            'clip_min_y': cum.clip_min_y,
            'clip_max_x': cum.clip_max_x,
            'clip_max_y': cum.clip_max_y,
            'black_level': jsonEx.colorToJson(cum.black_level),
            'white_level': jsonEx.colorToJson(cum.white_level),
            'curves': []
        }
        for curveMap in cum.curves:
            rez['curves'].append(CurveMap.cmToJson(curveMap))
        return rez
    @staticmethod
    def jsonToCum(cum, cumInJson):
        jsonEx = JsonEx.JsonEx
        cum.use_clip = cumInJson['use_clip']
        cum.clip_min_x = cumInJson['clip_min_x']
        cum.clip_min_y = cumInJson['clip_min_y']
        cum.clip_max_x = cumInJson['clip_max_x']
        cum.clip_max_y = cumInJson['clip_max_y']
        jsonEx.colorLoadFromJson(cum.black_level, cumInJson['black_level'])
        jsonEx.colorLoadFromJson(cum.white_level, cumInJson['white_level'])
        for i, curve in enumerate(cumInJson['curves']):
            CurveMap.jsonToCm(cum.curves[i], curve)
        cum.update()


# CurveMap (curve)
class CurveMap():
    @staticmethod
    def cmToJson(cm):
        rez = {
            'extend': cm.extend,
            'points': []
        }
        for point in cm.points:
            rez['points'].append(CurveMapPoint.cmpToJson(point))
        return rez
    @staticmethod
    def jsonToCm(cm, cmInJson):
        cm.extend = cmInJson['extend']
        for i, point in enumerate(cmInJson['points']):
            if len(cm.points) <= i:
                cm.points.new(point['location'][0], point['location'][1])
            CurveMapPoint.jsonToCmp(cm.points[i], point)


# CurveMapPoint
class CurveMapPoint():
    @staticmethod
    def cmpToJson(cmp):
        jsonEx = JsonEx.JsonEx
        return {
            'location': jsonEx.vector2ToJson(cmp.location),
            'handle_type': cmp.handle_type,
            'select': cmp.select
        }
    @staticmethod
    def jsonToCmp(cmp, cmpInJson):
        jsonEx = JsonEx.JsonEx
        jsonEx.vector2LoadFromJson(cmp.location, cmpInJson['location'])
        cmp.handle_type = cmpInJson['handle_type']
        cmp.select = cmpInJson['select']


# Compositing
class NodeCompositorNodeGroup(NodeShaderNodeGroup):
    pass


# Node IO
class IOCommon():
    @staticmethod
    def ioToJson(io):
        return {
            'type': io.type,
            'bl_type': io.bl_idname,
            'name': io.name
        }
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        node.inputs[inputNumber].name = inputInJson['name']
    @staticmethod
    def jsonToO(node, outputNumber, outputInJson):
        node.outputs[outputNumber].name = outputInJson['name']


class IONodeSocketColor(IOCommon):
    @staticmethod
    def ioToJson(io):
        ioJson = super(__class__, __class__).ioToJson(io)
        jsonEx = JsonEx.JsonEx
        ioJson['default_value'] = jsonEx.propArrayToJson(io.default_value)
        return ioJson
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        super(__class__, __class__).jsonToI(node, inputNumber, inputInJson)
        jsonEx = JsonEx.JsonEx
        jsonEx.propArrayLoadFromJson(node.inputs[inputNumber].default_value, inputInJson['default_value'])
    @staticmethod
    def jsonToO(node, outputNumber, outputInJson):
        super(__class__, __class__).jsonToO(node, outputNumber, outputInJson)
        jsonEx = JsonEx.JsonEx
        jsonEx.propArrayLoadFromJson(node.outputs[outputNumber].default_value, outputInJson['default_value'])


class IONodeSocketVector(IONodeSocketColor):
    pass


class IONodeSocketVectorDirection(IONodeSocketColor):
    pass


class IONodeSocketShader(IOCommon):
    pass


class IONodeSocketVirtual(IOCommon):
    pass


class IONodeSocketFloat(IOCommon):
    @staticmethod
    def ioToJson(io):
        ioJson = super(__class__, __class__).ioToJson(io)
        ioJson['default_value'] = io.default_value
        return ioJson
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        super(__class__, __class__).jsonToI(node, inputNumber, inputInJson)
        node.inputs[inputNumber].default_value = inputInJson['default_value']
    @staticmethod
    def jsonToO(node, outputNumber, outputInJson):
        super(__class__, __class__).jsonToO(node, outputNumber, outputInJson)
        node.outputs[outputNumber].default_value = outputInJson['default_value']


class IONodeSocketFloatFactor(IONodeSocketFloat):
    pass


class IONodeSocketFloatAngle(IONodeSocketFloat):
    pass


class IONodeSocketFloatUnsigned(IONodeSocketFloat):
    pass


class IONodeSocketInt(IONodeSocketFloat):
    pass


class IONodeGroupInput():
    @staticmethod
    def ioToJson(io):
        return {}
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        pass
    def jsonToO(node, outputNumber, outputInJson):
        pass


class IONodeGroupOutput(IONodeGroupInput):
    pass


# Groupe IO
class GIOCommon():
    @staticmethod
    def gioToJson(io, gio = None):
        return {
            'type': io.type,
            'bl_type': io.bl_socket_idname,
            'name': io.name
        }
    @staticmethod
    def jsonToGi(nodeTree, groupNode, inputNumber, inputInJson):
        return nodeTree.inputs.new(type = inputInJson['bl_type'], name = inputInJson['name'])
    @staticmethod
    def jsonToGo(nodeTree, outputInJson):
        return nodeTree.outputs.new(type = outputInJson['bl_type'], name = outputInJson['name'])


class GIONodeSocketColor(GIOCommon):
    @staticmethod
    def gioToJson(io, gio = None):
        gioJson = super(__class__, __class__).gioToJson(io, gio)
        jsonEx = JsonEx.JsonEx
        gioJson['default_value'] = jsonEx.propArrayToJson(io.default_value)
        if gio:
            gioJson['value'] = jsonEx.propArrayToJson(gio.default_value)
        return gioJson
    @staticmethod
    def jsonToGi(nodeTree, groupNode, inputNumber, inputInJson):
        currentInput = super(__class__, __class__).jsonToGi(nodeTree, groupNode, inputNumber, inputInJson)
        jsonEx = JsonEx.JsonEx
        jsonEx.propArrayLoadFromJson(currentInput.default_value, inputInJson['default_value'])
        if inputInJson['value']:
            jsonEx.propArrayLoadFromJson(groupNode.inputs[inputNumber].default_value, inputInJson['value'])
        return currentInput
    @staticmethod
    def jsonToGo(nodeTree, outputInJson):
        currentOutput = super(__class__, __class__).jsonToGo(nodeTree, outputInJson)
        jsonEx = JsonEx.JsonEx
        jsonEx.propArrayLoadFromJson(currentOutput.default_value, outputInJson['default_value'])
        return currentOutput


class GIONodeSocketVector(GIONodeSocketColor):
    pass


class GIONodeSocketShader(GIOCommon):
    pass


class GIONodeSocketFloat(GIOCommon):
    @staticmethod
    def gioToJson(io, gio = None):
        gioJson = super(__class__, __class__).gioToJson(io, gio)
        gioJson['default_value'] = io.default_value
        gioJson['min_value'] = io.min_value
        gioJson['max_value'] = io.max_value
        if gio:
            gioJson['value'] = gio.default_value
        return gioJson
    @staticmethod
    def jsonToGi(nodeTree, groupNode, inputNumber, inputInJson):
        currentInput = super(__class__, __class__).jsonToGi(nodeTree, groupNode, inputNumber, inputInJson)
        currentInput.default_value = inputInJson['default_value']
        currentInput.min_value = inputInJson['min_value']
        currentInput.max_value = inputInJson['max_value']
        groupNode.inputs[inputNumber].default_value = inputInJson['value']
        return currentInput
    @staticmethod
    def jsonToGo(nodeTree, outputInJson):
        currentOutput = super(__class__, __class__).jsonToGo(nodeTree, outputInJson)
        currentOutput.default_value = outputInJson['default_value']
        return currentOutput


class GIONodeSocketFloatFactor(GIONodeSocketFloat):
    pass


class GIONodeSocketFloatAngle(GIONodeSocketFloat):
    pass


class GIONodeSocketFloatUnsigned(GIONodeSocketFloat):
    pass


class GIONodeSocketInt(GIONodeSocketFloat):
    pass
