# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

# File manager

import bpy
import json
import os
import re
import tempfile
import zipfile
from ntpath import basename
from shutil import copyfile
from . import cfg


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

    @classmethod
    def zip_files(cls, source_files_list, temp_dir, zip_name):
        # pack files to zip archive
        # source_files_list = [{'path': 'd:/xxx.jpg', 'name': 'xxx.jpg'}, ...]
        zip_file_name = zip_name + '.zip'
        zip_file_path = os.path.join(temp_dir, zip_file_name)
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for file_info in source_files_list:
                file_path = file_info['path'] if 'path' in file_info else ''
                if file_path and os.path.exists(file_path) and os.path.isfile(file_path):
                    file_name = file_info['name'] if 'name' in file_info else os.path.basename(file_path)
                    zip_file.write(
                        file_path,
                        compress_type=zipfile.ZIP_DEFLATED,
                        compresslevel=9,
                        arcname=cls.normalize_file_name(file_name)
                    )
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

    @staticmethod
    def project_name():
        # returns current opened project dir
        if bpy.data.filepath:
            return os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        else:
            return ''

    @classmethod
    def attachments_path(cls):
        # returns path to bis-attachments dir
        return os.path.join(cls.project_dir(), cls.project_name() + '_bis_external')

    # ----------------------------------------------------------
    # debug section
    # ----------------------------------------------------------

    @classmethod
    def json_to_file(cls, json_data, file_name):
        # save json data to file in project directory
        with open(os.path.join(cls.project_dir(), file_name), 'w') as currentFile:
            json.dump(json_data, currentFile, indent=4)

    @classmethod
    def attachment_to_file(cls, attachment_file_path):
        # save attachment file in project directory
        if os.path.exists(attachment_file_path):
            copyfile(
                attachment_file_path,
                os.path.join(cls.project_dir(), basename(attachment_file_path))
            )

    @classmethod
    def to_server_to_file(cls, json_data=None, attachment_file_path=None):
        # save data sending to server to file in project directory
        if cfg.to_server_to_file:
            if json_data:
                cls.json_to_file(
                    json_data=json_data,
                    file_name='send_to_server.json'
                )
            if attachment_file_path:
                cls.attachment_to_file(
                    attachment_file_path=attachment_file_path
                )

    @classmethod
    def from_server_to_file(cls, json_data=None, attachment_file_path=None):
        # save data received from server to file in project directory
        if cfg.from_server_to_file:
            if json_data:
                cls.json_to_file(
                    json_data=json_data,
                    file_name='received_from_server.json'
                )
            if attachment_file_path:
                cls.attachment_to_file(
                    attachment_file_path=attachment_file_path
                )

