# Nikita Akimov
# interplanety@interplanety.org

import bpy
from . import cfg
from .node_manager import NodeManager
from .material import Material
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
        default=True
    )

    def execute(self, context):
        rez = {"stat": "ERR", "data": {"text": "Undefined material item to save"}}
        data_to_save = None
        tags = ''
        subtype = Material.get_subtype(context=context)
        subtype2 = Material.get_subtype2(context=context)
        if subtype == 'ShaderNodeTree':
            if subtype2 == 'WORLD':
                tags = 'world'
            elif subtype2 == 'OBJECT':
                tags = 'shader'
        elif subtype == 'CompositorNodeTree':
            tags = 'compositing'
        # Save Node Group (in Compositor work only with Node Groups)
        if context.preferences.addons[__package__].preferences.use_node_group_as == 'NODEGROUP' or subtype == 'CompositorNodeTree':
            active_node = NodeManager.active_node(context=context)
            if active_node and active_node.type == 'GROUP':
                data_to_save = active_node  # save active node group
            else:
                rez['data']['text'] = 'No selected Node Group'
        # Save Material
        elif context.preferences.addons[__package__].preferences.use_node_group_as == 'MATERIAL':
            active_material = NodeManager.active_material(context=context)
            if active_material:
                data_to_save = active_material  # save active material
            else:
                rez['data']['text'] = 'No material to save'
        if data_to_save:
            if NodeManager.is_procedural(data_to_save):
                tags += (';' if tags else '') + 'procedural'
            tags += (';' if tags else '') + context.window.scene.render.engine
            tags += (';' if tags else '') + '{0[0]}.{0[1]}'.format(app.version)
            if context.window_manager.bis_add_nodegroup_to_storage_vars.tags != '':
                tags += (';' if tags else '') + context.window_manager.bis_add_nodegroup_to_storage_vars.tags
            rez = NodeManager.to_bis(context=context,
                                     item=data_to_save,
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
        name='Tags (comma separated)',
        description='Add some tags to describe this material',
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
