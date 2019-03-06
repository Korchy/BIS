# Nikita Akimov
# interplanety@interplanety.org

from bpy.props import StringProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class


class MessageBox(Operator):
    bl_idname = 'message.messagebox'
    bl_label = ''

    message: StringProperty(
        name='message',
        description='message',
        default=''
    )

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        if '\n' in self.message:
            lines = self.message.split('\n')
            for line in lines:
                layout.label(text=line.strip())
        else:
            layout.label(text=self.message)
        layout.separator()


def register():
    register_class(MessageBox)


def unregister():
    unregister_class(MessageBox)


if __name__ == '__main__':
    register()
