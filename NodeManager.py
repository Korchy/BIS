import json
import sys
import bpy

class NodeManager():

    @staticmethod
    def nodeGroupToJson(nodeGroup):
        if nodeGroup.type == 'GROUP':
            nodeGroupTree = nodeGroup.node_tree
            nodeGroupTreeNodes = nodeGroupTree.nodes
            groupInJson = json.loads('{"name": "", "nodes": [], "links": [], "GroupInput" : [], "GroupOutput" : []}')
            groupInJson['name'] = nodeGroupTree.name
            # indexing
            nodeGroupTreeNodesIndexed = []
            for node in nodeGroupTreeNodes:
                inputs = []
                for input in node.inputs:
                    inputs.append(input)
                outputs = []
                for output in node.outputs:
                    outputs.append(output)
                nodeGroupTreeNodesIndexed.append([node, inputs, outputs])
            # Nodes
            for node in nodeGroupTreeNodesIndexed:
                nodeClass = NodeCommon
                if hasattr(sys.modules[modulesNames['NodeManager']], 'Node' + node[0].bl_idname):
                    nodeClass = getattr(sys.modules[modulesNames['NodeManager']], 'Node' + node[0].bl_idname)
                currentNode = nodeClass.nodeToJson(node[0])
                for input in node[1]:
                    ioName = 'IO' + input.bl_idname
                    if node[0].bl_idname == 'NodeGroupInput' or node[0].bl_idname == 'NodeGroupOutput':
                        ioName = 'IO' + node[0].bl_idname
                    ioClass = IOCommon
                    if hasattr(sys.modules[modulesNames['NodeManager']], ioName):
                        ioClass = getattr(sys.modules[modulesNames['NodeManager']], ioName)
                    currentNode['inputs'].append(ioClass.ioToJson(input))
                for output in node[2]:
                    ioName = 'IO' + output.bl_idname
                    if node[0].bl_idname == 'NodeGroupInput' or node[0].bl_idname == 'NodeGroupOutput':
                        ioName = 'IO' + node[0].bl_idname
                    ioClass = IOCommon
                    if hasattr(sys.modules[modulesNames['NodeManager']], ioName):
                        ioClass = getattr(sys.modules[modulesNames['NodeManager']], ioName)
                    currentNode['outputs'].append(ioClass.ioToJson(output))
                groupInJson['nodes'].append(currentNode)
            # GroupInputs
            group_input_number = 0
            for input in nodeGroupTree.inputs:
                gioClass = GIOCommon
                if hasattr(sys.modules[modulesNames['NodeManager']], 'GIO' + input.bl_socket_idname):
                    gioClass = getattr(sys.modules[modulesNames['NodeManager']], 'GIO' + input.bl_socket_idname)
                groupInJson['GroupInput'].append(gioClass.gioToJson(input, nodeGroup.inputs[group_input_number]))
                group_input_number += 1
            # GroupOutputs
            for output in nodeGroupTree.outputs:
                gioClass = GIOCommon
                if hasattr(sys.modules[modulesNames['NodeManager']], 'GIO' + output.bl_socket_idname):
                    gioClass = getattr(sys.modules[modulesNames['NodeManager']], 'GIO' + output.bl_socket_idname)
                groupInJson['GroupOutput'].append(gioClass.gioToJson(output))
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
                groupInJson['links'].append([fromNodeIndex, fromNodeOutputIndex, toNodeIndex, toNodeInputIndex])
            return groupInJson

    @staticmethod
    def jsonToNodeGroup(jsonNodeGroup):
        groupInJson = json.loads(jsonNodeGroup)
        group = bpy.data.node_groups.new(type = 'ShaderNodeTree', name = groupInJson['name'])
        groupNode = bpy.context.object.active_material.node_tree.nodes.new(type = 'ShaderNodeGroup')
        groupNode.location = (0, 0)
        groupNode.node_tree = group
        nodeGroupTreeNodesIndexed = []
        # GroupInputs
        inputNumber = 0
        for inputInJson in groupInJson['GroupInput']:
            gioClass = GIOCommon
            if hasattr(sys.modules[modulesNames['NodeManager']], 'GIO' + inputInJson['bl_type']):
                gioClass = getattr(sys.modules[modulesNames['NodeManager']], 'GIO' + inputInJson['bl_type'])
            gioClass.jsonToGi(group = group,
                              groupNode = groupNode,
                              inputNumber = inputNumber,
                              inputInJson = inputInJson)
            inputNumber += 1
        # GroupOutputs
        for outputInJson in groupInJson['GroupOutput']:
            gioClass = GIOCommon
            if hasattr(sys.modules[modulesNames['NodeManager']], 'GIO' + outputInJson['bl_type']):
                gioClass = getattr(sys.modules[modulesNames['NodeManager']], 'GIO' + outputInJson['bl_type'])
            gioClass.jsonToGo(group = group,
                              outputInJson = outputInJson)
        # Nodes
        for nodeInJson in groupInJson['nodes']:
            currentNode = None
            nodeClass = NodeCommon
            if hasattr(sys.modules[modulesNames['NodeManager']], 'Node' + nodeInJson['bl_type']):
                nodeClass = getattr(sys.modules[modulesNames['NodeManager']], 'Node' + nodeInJson['bl_type'])
            currentNode = nodeClass.jsonToNode(group = group,
                                               nodeInJson = nodeInJson)
            if currentNode:
                # Node Inputs
                currentInputs = []
                inputNumber = 0
                for nodeInputInJson in nodeInJson['inputs']:
                    if nodeInputInJson:
                        ioClass = IOCommon
                        if hasattr(sys.modules[modulesNames['NodeManager']], 'IO' + nodeInputInJson['bl_type']):
                            ioClass = getattr(sys.modules[modulesNames['NodeManager']], 'IO' + nodeInputInJson['bl_type'])
                        ioClass.jsonToI(node = currentNode,
                                        inputNumber = inputNumber,
                                        inputInJson = nodeInputInJson)
                    currentInputs.append(currentNode.inputs[inputNumber])
                    inputNumber += 1
                # Node Outputs
                currentOutputs = []
                outputNumber = 0
                for nodeOutputInJson in nodeInJson['outputs']:
                    currentOutputs.append(currentNode.outputs[outputNumber])
                    outputNumber += 1
                nodeGroupTreeNodesIndexed.append([currentInputs, currentOutputs])
        # Links
        for linkInJson in groupInJson['links']:
            fromOutput = nodeGroupTreeNodesIndexed[linkInJson[0]][1][linkInJson[1]]
            toInput = nodeGroupTreeNodesIndexed[linkInJson[2]][0][linkInJson[3]]
            group.links.new(fromOutput, toInput)
        return group

# Node
class NodeCommon():
    @staticmethod
    def nodeToJson(node):
        return {
            'type': node.type,
            'bl_type': node.bl_idname,
            'name': node.name,
            'label': node.label,
            'hide': node.hide,
            'location': [
                node.location.x,
                node.location.y
            ],
            'inputs': [],
            'outputs': []
        }
    @staticmethod
    def jsonToNode(group, nodeInJson):
        currentNode = group.nodes.new(type = nodeInJson['bl_type'])
        currentNode.name = nodeInJson['name']
        currentNode.hide = nodeInJson['hide']
        currentNode.label = nodeInJson['label']
        currentNode.location.x = nodeInJson['location'][0]
        currentNode.location.y = nodeInJson['location'][1]
        return currentNode

class NodeShaderNodeBsdfGlossy(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(NodeShaderNodeBsdfGlossy, NodeShaderNodeBsdfGlossy).nodeToJson(node)
        nodeJson['distribution'] = node.distribution
        return nodeJson
    @staticmethod
    def jsonToNode(group, nodeInJson):
        currentNode = super(NodeShaderNodeBsdfGlossy, NodeShaderNodeBsdfGlossy).jsonToNode(group, nodeInJson)
        currentNode.distribution = nodeInJson['distribution']
        return currentNode

class NodeShaderNodeAttribute(NodeCommon):
    @staticmethod
    def nodeToJson(node):
        nodeJson = super(NodeShaderNodeAttribute, NodeShaderNodeAttribute).nodeToJson(node)
        nodeJson['attribute_name'] = node.attribute_name
        return nodeJson
    @staticmethod
    def jsonToNode(group, nodeInJson):
        currentNode = super(NodeShaderNodeAttribute, NodeShaderNodeAttribute).jsonToNode(group, nodeInJson)
        currentNode.attribute_name = nodeInJson['attribute_name']
        return currentNode

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
        node.inputs[inputNumber].name = inputInJson['type']

class IONodeSocketColor(IOCommon):
    @staticmethod
    def ioToJson(io):
        ioJson = super(IONodeSocketColor, IONodeSocketColor).ioToJson(io)
        ioJson['default_value'] = [
            io.default_value[0],
            io.default_value[1],
            io.default_value[2],
            io.default_value[3]
        ]
        return ioJson
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        super(IONodeSocketColor, IONodeSocketColor).jsonToI(node, inputNumber, inputInJson)
        node.inputs[inputNumber].default_value[0] = inputInJson['default_value'][0]
        node.inputs[inputNumber].default_value[1] = inputInJson['default_value'][1]
        node.inputs[inputNumber].default_value[2] = inputInJson['default_value'][2]
        node.inputs[inputNumber].default_value[3] = inputInJson['default_value'][3]

class IONodeSocketVector(IOCommon):
    @staticmethod
    def ioToJson(io):
        ioJson = super(IONodeSocketVector, IONodeSocketVector).ioToJson(io)
        ioJson['default_value'] = [
            io.default_value[0],
            io.default_value[1],
            io.default_value[2]
        ]
        return ioJson
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        super(IONodeSocketColor, IONodeSocketColor).jsonToI(node, inputNumber, inputInJson)
        node.inputs[inputNumber].default_value[0] = inputInJson['default_value'][0]
        node.inputs[inputNumber].default_value[1] = inputInJson['default_value'][1]
        node.inputs[inputNumber].default_value[2] = inputInJson['default_value'][2]

class IONodeSocketShader(IOCommon):
    pass

class IONodeSocketVirtual(IOCommon):
    pass

class IONodeSocketFloat(IOCommon):
    @staticmethod
    def ioToJson(io):
        ioJson = super(IONodeSocketFloat, IONodeSocketFloat).ioToJson(io)
        ioJson['default_value'] = io.default_value
        return ioJson
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        super(IONodeSocketColor, IONodeSocketColor).jsonToI(node, inputNumber, inputInJson)
        node.inputs[inputNumber].default_value = inputInJson['default_value']

class IONodeSocketFloatFactor(IONodeSocketFloat):
    pass

class IONodeGroupInput():
    @staticmethod
    def ioToJson(io):
        return {}
    @staticmethod
    def jsonToI(node, inputNumber, inputInJson):
        pass

class IONodeGroupOutput(IONodeGroupInput):
    pass

#Groupe IO
class GIOCommon():
    @staticmethod
    def gioToJson(io, gio = None):
        return {
            'type': io.type,
            'bl_type': io.bl_socket_idname,
            'name': io.name
        }
    @staticmethod
    def jsonToGi(group, groupNode, inputNumber, inputInJson):
        return group.inputs.new(type = inputInJson['bl_type'], name = inputInJson['name'])
    @staticmethod
    def jsonToGo(group, outputInJson):
        return group.outputs.new(type = outputInJson['bl_type'], name = outputInJson['name'])

class GIONodeSocketColor(GIOCommon):
    @staticmethod
    def gioToJson(io, gio = None):
        gioJson = super(GIONodeSocketColor, GIONodeSocketColor).gioToJson(io, gio)
        gioJson['default_value'] = [
            io.default_value[0],
            io.default_value[1],
            io.default_value[2],
            io.default_value[3]
        ]
        if gio:
            gioJson['value'] = [
                gio.default_value[0],
                gio.default_value[1],
                gio.default_value[2],
                gio.default_value[3]
            ]
        return gioJson
    @staticmethod
    def jsonToGi(group, groupNode, inputNumber, inputInJson):
        currentInput = super(GIONodeSocketColor, GIONodeSocketColor).jsonToGi(group, groupNode, inputNumber, inputInJson)
        currentInput.default_value[0] = inputInJson['default_value'][0]
        currentInput.default_value[1] = inputInJson['default_value'][1]
        currentInput.default_value[2] = inputInJson['default_value'][2]
        currentInput.default_value[3] = inputInJson['default_value'][3]
        groupNode.inputs[inputNumber].default_value[0] = inputInJson['value'][0]
        groupNode.inputs[inputNumber].default_value[1] = inputInJson['value'][1]
        groupNode.inputs[inputNumber].default_value[2] = inputInJson['value'][2]
        groupNode.inputs[inputNumber].default_value[3] = inputInJson['value'][3]
        return currentInput
    @staticmethod
    def jsonToGo(group, outputInJson):
        currentOutput = super(GIONodeSocketColor, GIONodeSocketColor).jsonToGo(group, outputInJson)
        currentOutput.default_value[0] = outputInJson['default_value'][0]
        currentOutput.default_value[1] = outputInJson['default_value'][1]
        currentOutput.default_value[2] = outputInJson['default_value'][2]
        currentOutput.default_value[3] = outputInJson['default_value'][3]
        return currentOutput

class GIONodeSocketVector(GIOCommon):
    @staticmethod
    def gioToJson(io, gio = None):
        gioJson = super(GIONodeSocketColor, GIONodeSocketColor).gioToJson(io, gio)
        gioJson['default_value'] = [
            io.default_value[0],
            io.default_value[1],
            io.default_value[2]
        ]
        if gio:
            gioJson['value'] = [
                gio.default_value[0],
                gio.default_value[1],
                gio.default_value[2]
            ]
        return gioJson
    @staticmethod
    def jsonToGi(group, groupNode, inputNumber, inputInJson):
        currentInput = super(GIONodeSocketColor, GIONodeSocketColor).jsonToGi(group, groupNode, inputNumber, inputInJson)
        currentInput.default_value[0] = inputInJson['default_value'][0]
        currentInput.default_value[1] = inputInJson['default_value'][1]
        currentInput.default_value[2] = inputInJson['default_value'][2]
        groupNode.inputs[inputNumber].default_value[0] = inputInJson['value'][0]
        groupNode.inputs[inputNumber].default_value[1] = inputInJson['value'][1]
        groupNode.inputs[inputNumber].default_value[2] = inputInJson['value'][2]
        return currentInput
    @staticmethod
    def jsonToGo(group, outputInJson):
        currentOutput = super(GIONodeSocketColor, GIONodeSocketColor).jsonToGo(group, outputInJson)
        currentOutput.default_value[0] = outputInJson['default_value'][0]
        currentOutput.default_value[1] = outputInJson['default_value'][1]
        currentOutput.default_value[2] = outputInJson['default_value'][2]
        return currentOutput

class GIONodeSocketShader(GIOCommon):
    pass

class GIONodeSocketFloat(GIOCommon):
    @staticmethod
    def gioToJson(io, gio = None):
        gioJson = super(GIONodeSocketFloat, GIONodeSocketFloat).gioToJson(io, gio)
        gioJson['default_value'] = io.default_value
        gioJson['min_value'] = io.min_value
        gioJson['max_value'] = io.max_value
        gioJson['default_value'] = io.default_value
        if gio:
            gioJson['value'] = gio.default_value
        return gioJson
    @staticmethod
    def jsonToGi(group, groupNode, inputNumber, inputInJson):
        currentInput = super(GIONodeSocketColor, GIONodeSocketColor).jsonToGi(group, groupNode, inputNumber, inputInJson)
        currentInput.default_value = inputInJson['default_value']
        currentInput.min_value = inputInJson['min_value']
        currentInput.max_value = inputInJson['max_value']
        groupNode.inputs[inputNumber].default_value = inputInJson['value']
        return currentInput
    @staticmethod
    def jsonToGo(group, outputInJson):
        currentOutput = super(GIONodeSocketColor, GIONodeSocketColor).jsonToGo(group, outputInJson)
        currentOutput.default_value = outputInJson['default_value']
        return currentOutput

class GIONodeSocketFloatFactor(GIONodeSocketFloat):
    pass
