# Nikita Akimov
# interplanety@interplanety.org

from bpy.types import Panel
from bpy.utils import register_class, unregister_class


class BISMeshPanel(Panel):
    bl_idname = 'BIS_PT_mesh_panel'
    bl_label = 'BIS - MESHES'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BIS'

    def draw(self, context):
        layout = self.layout
        if getattr(context.window_manager, __package__.lower()+'_web_auth_vars').logged:
            row = layout.row(align=True)
            row.label(text='')
            help_button = row.operator('message.messagebox', icon='HELP')
            help_button.width = 600
            help_button.message = '- Why I can not get materials?\n' \
                                  'This panel is for MESHES! Switch to the Shader Editor window to get materials.\n\n' \
                                  '- Please do not save Plane with material / Cube with material / Sphere with material to save your materials.\n' \
                                  ' This saves only meshes. To save your materials switch to the Shader Editor window.'
            if getattr(context.window_manager, __package__.lower()+'_web_auth_vars').userProStatus:
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
            layout.label(text='(comma separated)')
            button = layout.operator('bis.add_mesh_to_storage', text='Save as New')
            button.show_message = True
            button = layout.operator('bis.update_mesh_in_storage', text='Update')
            button.show_message = True
            layout.separator()
            layout.separator()
            layout.operator('bis.web_auth', icon='FILE_TICK', text='Sign out')
        else:
            layout.operator('bis.web_auth', icon='WORLD', text='Sign in')


def register():
    register_class(BISMeshPanel)


def unregister():
    unregister_class(BISMeshPanel)
