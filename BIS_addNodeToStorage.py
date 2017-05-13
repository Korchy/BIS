import bpy
import sys
import json

class BIS_addNodeToStorage(bpy.types.Operator):
    bl_idname = 'bis.add_node_to_storage'
    bl_label = 'BIS_AddToIStorage'
    bl_description = 'Add nodegroup to common part of BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if(bpy.context.active_node and bpy.context.active_node.type == 'GROUP'):    # context.active_node - ShaderNodeGroup
            nodeGroupJson = sys.modules[modulesNames['NodeManager']].NodeManager.nodeGroupToJson(bpy.context.active_object.active_material.node_tree.nodes.active)
            request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                'for': 'set_node_group',
                'node_group': json.dumps(nodeGroupJson),
                'node_group_name': nodeGroupJson['name'],
                'node_group_tags': bpy.context.scene.bis_add_node_to_storage_vars.tags
            })
            bpy.context.scene.bis_add_node_to_storage_vars.tags = ''
            requestRez = json.loads(request.text)
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = requestRez['stat'])
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = 'No NodeGroup selected')
        return {'FINISHED'}

class BIS_addNodeToStorageVars(bpy.types.PropertyGroup):
    tags = bpy.props.StringProperty(
        name = 'Tags',
        description = 'Tags',
        default = ''
    )

def register():
    bpy.utils.register_class(BIS_addNodeToStorage)
    bpy.utils.register_class(BIS_addNodeToStorageVars)
    bpy.types.Scene.bis_add_node_to_storage_vars = bpy.props.PointerProperty(type = BIS_addNodeToStorageVars)

def unregister():
    del bpy.types.Scene.bis_add_node_to_storage_vars
    bpy.utils.unregister_class(BIS_addNodeToStorageVars)
    bpy.utils.unregister_class(BIS_addNodeToStorage)
