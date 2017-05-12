import bpy
import sys
import json

class BIS_addNodeToStore(bpy.types.Operator):
    bl_idname = 'bis.add_node_to_store'
    bl_label = 'BIS_AddToIStore'
    bl_description = 'Add nodegroup to common part of BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if(bpy.context.active_node and bpy.context.active_node.type == 'GROUP'):    # context.active_node - ShaderNodeGroup
            nodeGroupJson = sys.modules[modulesNames['NodeManager']].NodeManager.nodeGroupToJson(bpy.context.active_object.active_material.node_tree.nodes.active)
            request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                'for': 'set_node_group',
                'node_group': json.dumps(nodeGroupJson),
                'node_group_name': nodeGroupJson['name'],
                'node_group_tags': bpy.context.scene.bis_add_node_to_store_vars.tags
            })
            bpy.context.scene.bis_add_node_to_store_vars.tags = ''
            requestRez = json.loads(request.text)
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = requestRez['stat'])
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = 'No NodeGroup selected')
        return {'FINISHED'}

class BIS_addNodeToStoreVars(bpy.types.PropertyGroup):
    tags = bpy.props.StringProperty(
        name = 'Tags',
        description = 'Tags',
        default = ''
    )

def register():
    bpy.utils.register_class(BIS_addNodeToStore)
    bpy.utils.register_class(BIS_addNodeToStoreVars)
    bpy.types.Scene.bis_add_node_to_store_vars = bpy.props.PointerProperty(type = BIS_addNodeToStoreVars)

def unregister():
    del bpy.types.Scene.bis_add_nodes_to_store_vars
    bpy.utils.unregister_class(BIS_addNodeToStoreVars)
    bpy.utils.unregister_class(BIS_addNodeToStore)
