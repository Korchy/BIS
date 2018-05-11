# Nikita Akimov
# interplanety@interplanety.org

import bpy
import json
from . import WebRequests
from . import NodeManager


class BIS_getNodeFromStorage(bpy.types.Operator):
    bl_idname = 'bis.get_nodegroup_from_storage'
    bl_label = 'BIS_GetFromStorage'
    bl_description = 'Get nodegroup from common part of BIS'
    bl_options = {'REGISTER', 'UNDO'}

    nodeGroupId = bpy.props.IntProperty(
        name='NodeGroupId',
        default=0
    )

    def execute(self, context):
        if self.nodeGroupId:
            request = WebRequests.WebRequest.sendRequest({
                'for': 'get_node_group',
                'id': self.nodeGroupId
            })
            if request:
                requestRez = json.loads(request.text)
                if requestRez['stat'] != 'OK':
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=requestRez['data']['text'])
                else:
                    nodeInJson = json.loads(requestRez['data']['item'])
                    destNodeTree = None
                    if nodeInJson['bl_type'] == 'CompositorNodeGroup':
                        if context.area.spaces.active.node_tree.bl_idname == 'CompositorNodeTree':
                            destNodeTree = context.area.spaces.active.node_tree
                            if not context.screen.scene.use_nodes:
                                context.screen.scene.use_nodes = True
                    elif nodeInJson['bl_type'] == 'ShaderNodeGroup':
                        if context.active_object:
                            if not context.active_object.active_material:
                                context.active_object.active_material = bpy.data.materials.new(name='Material')
                                context.active_object.active_material.use_nodes = True
                                for currentNode in context.active_object.active_material.node_tree.nodes:
                                    if currentNode.bl_idname != 'ShaderNodeOutputMaterial':
                                        context.active_object.active_material.node_tree.nodes.remove(currentNode)
                            if context.area.spaces.active.tree_type == 'ShaderNodeTree':
                                destNodeTree = context.active_object.active_material.node_tree
                    if nodeInJson and destNodeTree:
                        NodeManager.NodeManager.jsonToNodeGroup(destNodeTree, nodeInJson)
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message='No NodeGroup To Get')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(BIS_getNodeFromStorage)


def unregister():
    bpy.utils.unregister_class(BIS_getNodeFromStorage)
