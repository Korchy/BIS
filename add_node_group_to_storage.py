# Nikita Akimov
# interplanety@interplanety.org

import bpy
from . import cfg
from .node_manager import NodeManager
from bpy.utils import register_class, unregister_class
from bpy.props import PointerProperty, BoolProperty
from bpy.types import Operator, PropertyGroup, WindowManager
from bpy import app


class BISAddNodeToStorage(Operator):
    bl_idname = 'bis.add_nodegroup_to_storage'
    bl_label = 'BIS_AddToIStorage'
    bl_description = 'Add nodegroup to the BIS'
    bl_options = {'REGISTER', 'UNDO'}

    show_message: BoolProperty(
        default=False
    )

    def execute(self, context):
        data_to_save = None
        tags = ''
        rez = {"stat": "ERR", "data": {"text": "Undefined material item to save"}}
        if context.preferences.addons[__package__].preferences.use_node_group_as == 'NODEGROUP':
            active_node = NodeManager.active_node(context=context)
            if active_node and active_node.type == 'GROUP':
                data_to_save = active_node  # save active node
                if NodeManager.get_subtype(context) == 'ShaderNodeTree':
                    if NodeManager.get_subtype2(context=context) == 'WORLD':
                        tags = 'world'
                    elif NodeManager.get_subtype2(context=context) == 'OBJECT':
                        tags = 'shader'
                elif NodeManager.get_subtype(context) == 'CompositorNodeTree':
                    tags = 'compositing'
                if NodeManager.is_procedural(active_node):
                    tags += (';' if tags else '') + 'procedural'
                tags += (';' if tags else '') + context.window.scene.render.engine
                tags += (';' if tags else '') + '{0[0]}.{0[1]}'.format(app.version)
            else:
                rez['data']['text'] = 'No selected Node Group'
        elif context.preferences.addons[__package__].preferences.use_node_group_as == 'MATERIAL':

            pass

        if data_to_save:
            if context.window_manager.bis_add_nodegroup_to_storage_vars.tags != '':
                tags += (';' if tags else '') + context.window_manager.bis_add_nodegroup_to_storage_vars.tags
            rez = NodeManager.to_bis(context=context,
                                     data=data_to_save,
                                     item_type=context.preferences.addons[__package__].preferences.use_node_group_as,
                                     tags=tags
                                     )
        if rez['stat'] == 'OK':
            context.window_manager.bis_add_nodegroup_to_storage_vars.tags = ''
        else:
            if cfg.show_debug_err:
                print(rez['stat'] + ': ' + rez['data']['text'])
        if self.show_message:
            bpy.ops.message.messagebox('INVOKE_DEFAULT', message=rez['stat'] + ': ' + rez['data']['text'])
        return {'FINISHED'}


class BISAddNodeGroupToStorageVars(PropertyGroup):
    tags: bpy.props.StringProperty(
        name='Tags',
        description='Tags (comma separated)',
        default=''
    )


def register():
    register_class(BISAddNodeToStorage)
    register_class(BISAddNodeGroupToStorageVars)
    WindowManager.bis_add_nodegroup_to_storage_vars = PointerProperty(type=BISAddNodeGroupToStorageVars)


def unregister():
    del WindowManager.bis_add_nodegroup_to_storage_vars
    unregister_class(BISAddNodeGroupToStorageVars)
    unregister_class(BISAddNodeToStorage)
