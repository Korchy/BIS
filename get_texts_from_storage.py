# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


from bpy.props import PointerProperty, StringProperty, EnumProperty, IntProperty
from bpy.types import Operator, PropertyGroup, WindowManager
from bpy.utils import register_class, unregister_class
from .bis_items import BISItems
from .TextManager import TextManager


class BISGetTextsInfoFromStorage(Operator):
    bl_idname = 'bis.get_texts_info_from_storage'
    bl_label = 'BIS: get items'
    bl_description = 'Search texts in BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        TextManager.items_from_bis(
            context,
            search_filter=context.window_manager.bis_get_texts_info_from_storage_vars.search_filter,
            page=0
        )
        return {'FINISHED'}


class BISGetTextsInfoFromStoragePrevPage(Operator):
    bl_idname = 'bis.get_texts_info_from_storage_prev_page'
    bl_label = 'BIS: get items'
    bl_description = 'Get prev page'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        TextManager.items_from_bis(
            context,
            search_filter=context.window_manager.bis_get_texts_info_from_storage_vars.search_filter,
            page=context.window_manager.bis_get_texts_info_from_storage_vars.current_page - 1
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bis_get_texts_info_from_storage_vars.current_page > 0


class BISGetTextsInfoFromStorageNextPage(Operator):
    bl_idname = 'bis.get_texts_info_from_storage_next_page'
    bl_label = 'BIS: get items'
    bl_description = 'Get next page'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        TextManager.items_from_bis(
            context,
            search_filter=context.window_manager.bis_get_texts_info_from_storage_vars.search_filter,
            page=context.window_manager.bis_get_texts_info_from_storage_vars.current_page + 1
        )
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return context.window_manager.bis_get_texts_info_from_storage_vars.current_page_status not in ('', 'EOF')


class BISGetTextsInfoFromStorageVars(PropertyGroup):
    search_filter: StringProperty(
        name='Search',
        description='Filter to search',
        default=''
    )
    items: EnumProperty(
        items=lambda self, context: BISItems.get_previews(TextManager.storage_type()),
        update=lambda self, context: BISItems.on_preview_select(self, TextManager.storage_type())
    )
    current_page: IntProperty(
        default=0
    )
    current_page_status: StringProperty(
        default=''
    )


def register():
    register_class(BISGetTextsInfoFromStorage)
    register_class(BISGetTextsInfoFromStoragePrevPage)
    register_class(BISGetTextsInfoFromStorageNextPage)
    register_class(BISGetTextsInfoFromStorageVars)
    WindowManager.bis_get_texts_info_from_storage_vars = PointerProperty(type=BISGetTextsInfoFromStorageVars)


def unregister():
    del WindowManager.bis_get_texts_info_from_storage_vars
    unregister_class(BISGetTextsInfoFromStorageVars)
    unregister_class(BISGetTextsInfoFromStorageNextPage)
    unregister_class(BISGetTextsInfoFromStoragePrevPage)
    unregister_class(BISGetTextsInfoFromStorage)
