# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS


import os
import bpy
import zipfile
from .file_manager import FileManager


class DataBlockManager:

    # abstract class for common data block for saving/loading it in BIS

    _limit_file_size = 3*1024*1024     # max exported to .blend and zipped file size (3 Mb)

    @classmethod
    def export_to_blend(cls, context, data_block: set, export_path: str, export_file_name: str):
        # saves data block to the export_path directory in a *.blend format and zip it. Returns full path to the file
        rez = None
        if data_block:
            file_name = export_file_name + '.blend'
            file_path = os.path.join(export_path, file_name)
            context.blend_data.libraries.write(file_path, data_block)
            if os.path.exists(file_path):
                zip_file_name = export_file_name + '.zip'
                zip_file_path = os.path.join(export_path, zip_file_name)
                zip_file = zipfile.ZipFile(zip_file_path, 'w')
                zip_file.write(
                    filename=file_path,
                    compress_type=zipfile.ZIP_DEFLATED,
                    arcname=file_name
                )
                zip_file.close()
                if os.path.exists(zip_file_path):
                    if os.stat(zip_file_path).st_size < cls._limit_file_size:
                        rez = zip_file_path
                    else:
                        bpy.ops.bis.messagebox(
                            'INVOKE_DEFAULT',
                            message='ERR: Saving meshes must be less ' +
                                    str(round(cls._limit_file_size/1024/1024)) +
                                    ' Mb after zip export'
                        )
        else:
            bpy.ops.bis.messagebox('INVOKE_DEFAULT', message='ERR: No data to save')
        return rez

    @classmethod
    def import_from_blend(cls, context, zip_file_path, file_name, data_block_type, data_block_name=None):
        # add meshes to scene from zipped archive with *.blend file
        rez = []
        # import data block from .blend file
        if os.path.exists(zip_file_path):
            path = os.path.dirname(zip_file_path)
            full_path = os.path.join(path, file_name + '.blend')
            FileManager.unzip_files(
                source_zip_path=zip_file_path,
                dest_dir=path
            )
            if os.path.exists(full_path):
                with bpy.data.libraries.load(full_path) as (data_from, data_to):
                    if data_block_name is None:
                        setattr(
                            data_to,
                            data_block_type,
                            getattr(data_from, data_block_type)
                        )
                    else:
                        setattr(
                            data_to,
                            data_block_type,
                            [name for name in getattr(data_from, data_block_type) if name == data_block_name]
                        )
                    rez = getattr(data_to, data_block_type)[:]  # list of data block names
        return rez
