import bpy
import sys
import json

class BIS_getNodeFromStorage(bpy.types.Operator):
    bl_idname = 'bis.get_node_from_storage'
    bl_label = 'BIS_GetFromStorage'
    bl_description = 'Get nodegroup from common part of BIS'
    bl_options = {'REGISTER', 'UNDO'}

    nodeGroupId = bpy.props.IntProperty(
        name = 'NodeGroupId',
        default = 0
    )

    def execute(self, context):
        if(self.nodeGroupId):
            request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                'for': 'get_node_group',
                'id': self.nodeGroupId
            })
            requestRez = json.loads(request.text)
            if requestRez['stat'] != 'OK':
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message = requestRez['stat']['text'])
            else:
                if bpy.context.active_object:
                    if not bpy.context.active_object.active_material:
                        bpy.context.active_object.active_material = bpy.data.materials.new(name = 'Material')
                        bpy.context.active_object.active_material.use_nodes = True
                        for currentNode in bpy.context.active_object.active_material.node_tree.nodes:
                            if currentNode.bl_idname != 'ShaderNodeOutputMaterial':
                                bpy.context.active_object.active_material.node_tree.nodes.remove(currentNode)
                    sys.modules[modulesNames['NodeManager']].NodeManager.jsonToNodeGroup(bpy.context.active_object.active_material.node_tree, requestRez['data']['item'])
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = 'No NodeGroup To Get')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(BIS_getNodeFromStorage)

def unregister():
    bpy.utils.unregister_class(BIS_getNodeFromStorage)
