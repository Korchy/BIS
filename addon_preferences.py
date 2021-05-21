# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

from bpy.types import AddonPreferences
from bpy.props import BoolProperty, EnumProperty
from bpy.utils import register_class, unregister_class
from . import nodes_bis_custom


class BISAddonPreferences(AddonPreferences):
    bl_idname = __package__

    # experimental mode
    experimental_mode: BoolProperty(
        name='Experimental mode',
        default=False,
        update=lambda self, context: self.experimental_mode_change(context)
    )
    # use saved BIS material as material or as node group
    use_node_group_as: EnumProperty(
        items=[
            ('NODEGROUP', 'Node Group', 'Node Group', '', 0),
            ('MATERIAL', 'Material', 'Material', '', 1)
        ],
        default='MATERIAL'
    )
    # default panel mode in 3D_VIEW window
    default_mode_in_3d_view: EnumProperty(
        items=[
            ('MESHES', 'Meshes', 'Meshes', '', 0),
            ('MATERIALS', 'Materials', 'Materials', '', 1)
        ],
        default='MATERIALS'
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text='Use BIS materials as:')
        row = layout.row()
        row.prop(self, 'use_node_group_as', expand=True)
        layout.label(text='Default mode in 3D_VIEW window:')
        row = layout.row()
        row.prop(self, 'default_mode_in_3d_view', expand=True)
        layout.separator()
        layout.prop(self, 'experimental_mode')

    def experimental_mode_change(self, context):
        if self.experimental_mode:
            nodes_bis_custom.register()
        else:
            nodes_bis_custom.unregister()


def register():
    register_class(BISAddonPreferences)


def unregister():
    unregister_class(BISAddonPreferences)
