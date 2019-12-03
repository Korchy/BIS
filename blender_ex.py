# Nikita Akimov
# interplanety@interplanety.org

import bpy


class BlenderEx:

    @staticmethod
    def version_str_short():
        return '.'.join(map(str, bpy.app.version[:2]))    # '2.81'
