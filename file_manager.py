# Nikita Akimov
# interplanety@interplanety.org

# File manager
import os
import re
import bpy


class FileManager:

    @staticmethod
    def abs_path(path):
        # returns absolute file path from path
        if path[:2] == '//':
            return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(bpy.data.filepath)), path[2:]))
        else:
            return os.path.abspath(path)

    @staticmethod
    def normalize_file_name(source_file_name):
        # returns corrected file name from name with index (xx.jpg.001 -> xx.001.jpg)
        regexp = re.compile(r'(\.\d{3}$)')
        splitted_name = list(filter(None, regexp.split(source_file_name)))
        if len(splitted_name) > 1:
            name_ext = os.path.splitext(splitted_name[0])
            return name_ext[0] + splitted_name[1] + name_ext[1]
        else:
            return source_file_name
