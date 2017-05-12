import bpy
import sys
import json
import bpy.utils.previews
import base64
import os

class BIS_getNodesInfoFromStore(bpy.types.Operator):
    bl_idname = 'bis.get_nodes_info_from_store'
    bl_label = 'BIS_AddToIStore'
    bl_description = 'Add nodegroup to common part of BIS'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
            'for': 'search_nodes',
            'search_filter': bpy.context.window_manager.bis_get_nodes_info_from_store_vars.searchFilter,
            'update_preview': bpy.context.window_manager.bis_get_nodes_info_from_store_vars.updatePreviews
        })
        searchRez = json.loads(request.text)
        if searchRez['stat'] == 'T':
            previewToUpdate = PreviewManager.updatePreviewsFromData(searchRez['data'])
            if previewToUpdate:
                request = sys.modules[modulesNames['WebRequests']].WebRequest.sendRequest({
                    'for': 'update_previews',
                    'preview_list': previewToUpdate
                })
                previewsUpdateRez = json.loads(request.text)
                if previewsUpdateRez['stat'] == 'T':
                    PreviewManager.updatePreviewsFromData(previewsUpdateRez['data'])

            PreviewManager.clearCollection()
            PreviewManager.createPreviews(searchRez['data'])
        return {'FINISHED'}

class PreviewManager():

    previewsPaths = []
    previewsItems = []
    previewsCollection = bpy.utils.previews.new()

    @staticmethod
    def unregister():
        PreviewManager.clearCollection()
        bpy.utils.previews.remove(PreviewManager.previewsCollection)

    @staticmethod
    def createPreviews(data):
        for itemInfo in data:
            path = PreviewManager.getPreviewPath(int(itemInfo['id']))
            if path not in PreviewManager.previewsPaths:
                name = itemInfo['name']
                thumb = PreviewManager.previewsCollection.load(path, path, 'IMAGE')
                PreviewManager.previewsItems.append((itemInfo['id'], name, "", thumb.icon_id, int(itemInfo['id'])))
                PreviewManager.previewsPaths.append(path)

    @staticmethod
    def getPreviews(self, context):
        if context is None:
            return []
        return PreviewManager.previewsItems

    @staticmethod
    def clearCollection():
        if PreviewManager.previewsCollection:
            PreviewManager.previewsCollection.clear()
            PreviewManager.previewsPaths.clear()
            PreviewManager.previewsItems.clear()

    @staticmethod
    def getPreviewRelativeDir(id):
        dir = 0
        while id > dir:
            dir += 10000
        return 'prev_ng' + os.path.sep + str(dir - (0 if dir == 0 else 10000)) + '-' + str(dir)

    @staticmethod
    def getPreviewDir(id):
        return os.path.dirname(__file__) + os.path.sep + PreviewManager.getPreviewRelativeDir(id)

    @staticmethod
    def getPreviewPath(id):
        return PreviewManager.getPreviewDir(id) + os.path.sep + str(id) + '.jpg'

    @staticmethod
    def updatePreviewsFromData(data):
        previewToUpdate = ''
        for prewiewInfo in data:
            previewDir = PreviewManager.getPreviewDir(int(prewiewInfo['id']))
            if prewiewInfo['preview']:
                previewContent = base64.b64decode(prewiewInfo['preview'])
                if not os.path.exists(previewDir):
                    os.makedirs(previewDir)
                with open(PreviewManager.getPreviewPath(int(prewiewInfo['id'])), 'wb') as currentPreview:
                    currentPreview.write(previewContent)
            else:
                if not os.path.exists(PreviewManager.getPreviewPath(int(prewiewInfo['id']))):
                    previewToUpdate += ('' if previewToUpdate == '' else ',') + prewiewInfo['id']
        return previewToUpdate

    @staticmethod
    def onPreviewSelect(self, context):
        bpy.ops.bis.get_node_from_store(nodeGroupId = int(self.previews))

class BIS_getNodesInfoFromStoreVars(bpy.types.PropertyGroup):
    searchFilter = bpy.props.StringProperty(
        name = 'Search',
        description = 'Filter to search',
        default = ''
    )
    updatePreviews = bpy.props.BoolProperty(
        name = 'Update Previews',
        description = 'Update previews from server',
        default = False
    )
    previews = bpy.props.EnumProperty(
        items = PreviewManager.getPreviews,
        update = PreviewManager.onPreviewSelect
    )

def register():
    bpy.utils.register_class(BIS_getNodesInfoFromStore)
    bpy.utils.register_class(BIS_getNodesInfoFromStoreVars)
    bpy.types.WindowManager.bis_get_nodes_info_from_store_vars = bpy.props.PointerProperty(type = BIS_getNodesInfoFromStoreVars)

def unregister():
    del bpy.types.WindowManager.bis_get_nodes_info_from_store_vars
    PreviewManager.unregister()
    bpy.utils.unregister_class(BIS_getNodesInfoFromStoreVars)
    bpy.utils.unregister_class(BIS_getNodesInfoFromStore)
