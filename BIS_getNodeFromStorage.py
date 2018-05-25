# Nikita Akimov
# interplanety@interplanety.org

import bpy
import json
from .WebRequests import WebRequest
from .NodeManager import NodeManager


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
            subtype = NodeManager.get_subtype(context)
            subtype2 = NodeManager.get_subtype2(context)
            request = WebRequest.sendRequest({
                'for': 'get_item',
                'storage': context.area.spaces.active.type,
                'storage_subtype': subtype,
                'storage_subtype2': subtype2,
                'id': self.nodeGroupId
            })
            if request:
                requestRez = json.loads(request.text)
                if requestRez['stat'] != 'OK':
                    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=requestRez['data']['text'])
                else:
                    nodeInJson = json.loads(requestRez['data']['item'])
                    dest_node_tree = None
                    if subtype == 'CompositorNodeTree':
                        dest_node_tree = context.area.spaces.active.node_tree
                        if not context.screen.scene.use_nodes:
                            context.screen.scene.use_nodes = True
                    elif subtype == 'ShaderNodeTree':
                        if context.active_object:
                            if not context.active_object.active_material:
                                context.active_object.active_material = bpy.data.materials.new(name='Material')
                                context.active_object.active_material.use_nodes = True
                                for currentNode in context.active_object.active_material.node_tree.nodes:
                                    if currentNode.bl_idname != 'ShaderNodeOutputMaterial':
                                        context.active_object.active_material.node_tree.nodes.remove(currentNode)
                            if subtype2 == 'OBJECT':
                                dest_node_tree = context.active_object.active_material.node_tree
                            elif subtype2 == 'WORLD':
                                dest_node_tree = context.scene.world.node_tree
                    if nodeInJson and dest_node_tree:
                        NodeManager.jsonToNodeGroup(dest_node_tree, nodeInJson)
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message='No NodeGroup To Get')
        return {'FINISHED'}


def register():
    bpy.utils.register_class(BIS_getNodeFromStorage)


def unregister():
    bpy.utils.unregister_class(BIS_getNodeFromStorage)
