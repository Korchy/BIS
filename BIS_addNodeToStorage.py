# Nikita Akimov
# interplanety@interplanety.org

import bpy
import sys
import json


class BIS_addNodeToStorage(bpy.types.Operator):
    bl_idname = 'bis.add_nodegroup_to_storage'
    bl_label = 'BIS_AddToIStorage'
    bl_description = 'Add nodegroup to common part of BIS'
    bl_options = {'REGISTER', 'UNDO'}

    showMessage = bpy.props.BoolProperty(
        default = False
    )

    def execute(self, context):
        if(bpy.context.active_node and bpy.context.active_node.type == 'GROUP'):
            activeNode = bpy.context.active_node
            nodeGroupTags = ''
            if bpy.context.area.spaces.active.tree_type == 'ShaderNodeTree':
                activeNode = bpy.context.active_object.active_material.node_tree.nodes.active
                nodeGroupTags = 'shader'
            elif bpy.context.area.spaces.active.tree_type == 'CompositorNodeTree':
                nodeGroupTags = 'compositing'
            nodeGroupJson = sys.modules[modulesNames['NodeManager']].NodeManager.nodeGroupToJson(activeNode)
            if nodeGroupJson:
                if bpy.context.scene.bis_add_nodegroup_to_storage_vars.tags != '':
                    nodeGroupTags += (';' if nodeGroupTags else '') + bpy.context.scene.bis_add_nodegroup_to_storage_vars.tags
                request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                    'for': 'set_node_group',
                    'node_group': json.dumps(nodeGroupJson),
                    'node_group_name': nodeGroupJson['name'],
                    'node_group_tags': (nodeGroupTags).strip()
                })
                if request:
                    bpy.context.scene.bis_add_nodegroup_to_storage_vars.tags = ''
                    requestRez = json.loads(request.text)
                    if self.showMessage:
                        bpy.ops.message.messagebox('INVOKE_DEFAULT', message = requestRez['stat'])
        else:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message = 'No NodeGroup selected')
        return {'FINISHED'}


class BIS_addNodeGroupToStorageVars(bpy.types.PropertyGroup):
    tags = bpy.props.StringProperty(
        name = 'Tags',
        description = 'Tags',
        default = ''
    )


def register():
    bpy.utils.register_class(BIS_addNodeToStorage)
    bpy.utils.register_class(BIS_addNodeGroupToStorageVars)
    bpy.types.Scene.bis_add_nodegroup_to_storage_vars = bpy.props.PointerProperty(type = BIS_addNodeGroupToStorageVars)


def unregister():
    del bpy.types.Scene.bis_add_nodegroup_to_storage_vars
    bpy.utils.unregister_class(BIS_addNodeGroupToStorageVars)
    bpy.utils.unregister_class(BIS_addNodeToStorage)
