import bpy
import sys

class BIS_addTextToStorage(bpy.types.Operator):
    bl_idname = 'bis.add_text_to_storage'
    bl_label = 'BIS_AddToStorage'
    bl_description = 'Add text to BIS'
    bl_options = {'REGISTER', 'UNDO'}

    textName = bpy.props.StringProperty(
        name = "textName",
        description = "Add text with current name",
        default = ''
    )
    showMessage = bpy.props.BoolProperty(
        default = False
    )

    def execute(self, context):
        if self.textName:
            currentText = bpy.data.texts[self.textName]
        else:
            currentText = bpy.context.area.spaces.active.text
        rez = sys.modules[modulesNames['TextManager']].TextManager.toBis(currentText, bpy.context.scene.bis_add_text_to_storage_vars.tags)
        if rez['stat'] == 'OK':
            bpy.context.scene.bis_add_text_to_storage_vars.tags = ''
            if self.showMessage:
                bpy.ops.message.messagebox('INVOKE_DEFAULT', message = rez['data']['text'])
        return {'FINISHED'}

class BIS_addTextToStorageVars(bpy.types.PropertyGroup):
    tags = bpy.props.StringProperty(
        name = 'Tags',
        description = 'Tags',
        default = ''
    )

def register():
    bpy.utils.register_class(BIS_addTextToStorage)
    bpy.utils.register_class(BIS_addTextToStorageVars)
    bpy.types.Scene.bis_add_text_to_storage_vars = bpy.props.PointerProperty(type = BIS_addTextToStorageVars)

def unregister():
    del bpy.types.Scene.bis_add_text_to_storage_vars
    bpy.utils.unregister_class(BIS_addTextToStorageVars)
    bpy.utils.unregister_class(BIS_addTextToStorage)
