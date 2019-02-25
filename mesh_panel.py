# Nikita Akimov
# interplanety@interplanety.org

from bpy.types import Panel
from bpy.utils import register_class, unregister_class
from . import WebRequests


class BISMeshPanel(Panel):
    bl_idname = 'bis.mesh_panel'
    bl_label = 'BIS - MESHES'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BIS'

    def draw(self, context):
        layout = self.layout
        if WebRequests.WebAuthVars.logged:
            if WebRequests.WebAuthVars.userProStatus:
                layout.prop(context.window_manager.bis_get_meshes_info_from_storage_vars, 'search_filter')
                layout.operator('bis.get_meshes_info_from_storage', icon='VIEWZOOM', text=' Search')
                row = layout.row()
                row.operator('bis.get_meshes_info_from_storage_prev_page', text='Prev')
                row.operator('bis.get_meshes_info_from_storage_next_page', text='Next')
            else:
                layout.operator('bis.get_meshes_info_from_storage', icon='FILE_REFRESH', text=' Get active palette')
            layout.prop(context.window_manager.bis_get_meshes_info_from_storage_vars, 'update_previews')
            layout.separator()
            layout.separator()
            layout.template_icon_view(context.window_manager.bis_get_meshes_info_from_storage_vars, 'items', show_labels=True)
            layout.separator()
            layout.separator()
            layout.prop(context.window_manager.bis_add_mesh_to_storage_vars, 'name')
            layout.prop(context.window_manager.bis_add_mesh_to_storage_vars, 'tags')
            layout.label(text='(comma separated)')
            button = layout.operator('bis.add_mesh_to_storage', text='Save')
            button.show_message = True
            button = layout.operator('bis.update_mesh_in_storage', text='Update')
            button.show_message = True
            layout.separator()
            layout.separator()
            layout.operator('dialog.web_auth', icon='FILE_TICK', text='Sign out')
        else:
            layout.operator('dialog.web_auth', icon='WORLD', text='Sign in')


def register():
    register_class(BISMeshPanel)


def unregister():
    unregister_class(BISMeshPanel)
