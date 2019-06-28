# Nikita Akimov
# interplanety@interplanety.org

# File manager
import os
import re
import tempfile
import zipfile
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

    @staticmethod
    def zip_files(source_files_list, temp_dir, zip_name):
        # pack files to zip archive
        # source_files_list = [{'path': 'd:/xxx.jpg', 'name': 'xxx.jpg'}, ...]
        zip_file_name = zip_name + '.zip'
        zip_file_path = os.path.join(temp_dir, zip_file_name)
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for file_info in source_files_list:
                file_path = file_info['path'] if 'path' in file_info else ''
                if file_path:
                    file_name = file_info['name'] if 'name' in file_info else os.path.basename(file_path)
                    zip_file.write(file_path, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9, arcname=__class__.normalize_file_name(file_name))
        return zip_file_path

    @staticmethod
    def unzip_files(source_zip_path, dest_dir):
        if source_zip_path and os.path.exists(source_zip_path):
            zip_file = zipfile.ZipFile(file=source_zip_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            zip_file.extractall(path=dest_dir)

    @staticmethod
    def project_dir():
        # return project directory
        if bpy.data.filepath:
            return os.path.dirname(bpy.data.filepath)
        else:
            return tempfile.gettempdir()
