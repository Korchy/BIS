# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from .WebRequests import WebAuthVars


class BISMeshPanel(Panel):
    bl_idname = 'BIS_PT_mesh_panel'
    bl_label = 'BIS'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BIS'

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(context.preferences.addons[__package__].preferences, 'default_mode_in_3d_view', expand=True)
        row.separator()
        help_button = row.operator('message.messagebox', icon='HELP')
        help_button.width = 600
        help_button.message = '- How can I save materials to the library?\n' \
                              'Switch to the Shader Editor window.\n\n' \
                              '- Please do not save Plane with material / Cube with material / Sphere with material to save your materials.\n' \
                              ' From this window you can save only meshes.'
        if WebAuthVars.logged:
            if context.preferences.addons[__package__].preferences.default_mode_in_3d_view == 'MATERIALS':
                # materials (simple)
                if WebAuthVars.userProStatus:
                    layout.prop(context.window_manager.bis_get_nodes_info_from_storage_vars, 'search_filter')
                    layout.operator('bis.get_nodes_info_from_storage', icon='VIEWZOOM', text=' Search')
                    row = layout.row()
                    row.operator('bis.get_nodes_info_from_storage_prev_page', text='Prev')
                    row.operator('bis.get_nodes_info_from_storage_next_page', text='Next')
                else:
                    layout.operator('bis.get_nodes_info_from_storage', icon='FILE_REFRESH', text=' Get active materials')
                layout.prop(context.window_manager.bis_get_nodes_info_from_storage_vars, 'update_previews')
                layout.separator()
                layout.separator()
                layout.template_icon_view(
                    context.window_manager.bis_get_nodes_info_from_storage_vars,
                    'items',
                    show_labels=True
                )
                layout.separator()
                layout.label(text='More options in the Shader Editor window')
            else:
                # meshes
                if WebAuthVars.userProStatus:
                    layout.prop(context.window_manager.bis_get_meshes_info_from_storage_vars, 'search_filter')
                    layout.operator('bis.get_meshes_info_from_storage', icon='VIEWZOOM', text=' Search')
                    row = layout.row()
                    row.operator('bis.get_meshes_info_from_storage_prev_page', text='Prev')
                    row.operator('bis.get_meshes_info_from_storage_next_page', text='Next')
                else:
                    layout.operator('bis.get_meshes_info_from_storage', icon='FILE_REFRESH', text=' Get active meshes')
                layout.prop(context.window_manager.bis_get_meshes_info_from_storage_vars, 'update_previews')
                layout.separator()
                layout.separator()
                layout.template_icon_view(context.window_manager.bis_get_meshes_info_from_storage_vars, 'items', show_labels=True)
                layout.separator()
                layout.separator()
                layout.prop(context.window_manager.bis_add_mesh_to_storage_vars, 'name')
                layout.prop(context.window_manager.bis_add_mesh_to_storage_vars, 'tags')
                button = layout.operator('bis.add_mesh_to_storage', text='Save as New')
                button.show_message = True
                button = layout.operator('bis.update_mesh_in_storage', text='Update')
                button.show_message = True
            layout.separator()
            layout.separator()
            layout.operator('bis.web_auth', icon='FILE_TICK', text='Sign out')
        else:
            layout.operator('bis.web_auth', icon='WORLD', text='Sign in')


class BIS_PT_tools_meshes_panel(Panel):
    bl_idname = 'BIS_PT_tools_meshes_panel'
    bl_label = 'Tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BIS'

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text='Materials')
        box.operator(operator='bis.materials_active_to_selected', text='Active to Selected')


def register():
    register_class(BISMeshPanel)
    register_class(BIS_PT_tools_meshes_panel)


def unregister():
    unregister_class(BIS_PT_tools_meshes_panel)
    unregister_class(BISMeshPanel)
