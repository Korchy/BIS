import bpy
import os
import base64
import bpy.utils.previews

class BIS_Items():

    itemsLists = {}

    @staticmethod
    def register():
        __class__.itemsLists['NODE_EDITOR'] = bpy.utils.previews.new()
        __class__.itemsLists['NODE_EDITOR'].items = []
        __class__.itemsLists['TEXT_EDITOR'] = bpy.utils.previews.new()
        __class__.itemsLists['TEXT_EDITOR'].items = []

    @staticmethod
    def unregister():
        for itemList in __class__.itemsLists.values():
            itemList.items.clear()
            bpy.utils.previews.remove(itemList)
        __class__.itemsLists.clear()

    @staticmethod
    def createItemsList(data, listName, previews = True):
        __class__.clearItemList(listName)
        for itemInfo in data:
            if previews:
                path = __class__.getPreviewPath(int(itemInfo['id']), listName)
                thumb = __class__.itemsLists[listName].load(path, path, 'IMAGE')
                __class__.itemsLists[listName].items.append((itemInfo['id'], itemInfo['name'], '', thumb.icon_id, int(itemInfo['id'])))
            else:
                __class__.itemsLists[listName].items.append((itemInfo['id'], itemInfo['name'], '', '', int(itemInfo['id'])))

    @staticmethod
    def getPreviews(self, context):
        if context:
            return __class__.itemsLists[context.area.spaces.active.type].items
        else:
            return []

    @staticmethod
    def clearItemList(name):
        __class__.itemsLists[name].clear()
        __class__.itemsLists[name].items.clear()

    @staticmethod
    def getPreviewRelativeDir(id, listName):
        dir = 0
        while id > dir:
            dir += 10000
        return 'previews' + os.path.sep + listName + os.path.sep + str(dir - (0 if dir == 0 else 10000)) + '-' + str(dir)

    @staticmethod
    def getPreviewDir(id, listName):
        return os.path.dirname(__file__) + os.path.sep + __class__.getPreviewRelativeDir(id, listName)

    @staticmethod
    def getPreviewPath(id, listName):
        return __class__.getPreviewDir(id, listName) + os.path.sep + str(id) + '.jpg'

    @staticmethod
    def updatePreviewsFromData(data, listName):
        previewToUpdate = ''
        for prewiewInfo in data:
            previewDir = __class__.getPreviewDir(int(prewiewInfo['id']), listName)
            if prewiewInfo['preview']:
                previewContent = base64.b64decode(prewiewInfo['preview'])
                if not os.path.exists(previewDir):
                    os.makedirs(previewDir)
                with open(__class__.getPreviewPath(int(prewiewInfo['id']), listName), 'wb') as currentPreview:
                    currentPreview.write(previewContent)
            else:
                if not os.path.exists(__class__.getPreviewPath(int(prewiewInfo['id']), listName)):
                    previewToUpdate += ('' if previewToUpdate == '' else ',') + prewiewInfo['id']
        return previewToUpdate

    @staticmethod
    def onPreviewSelect(self, context):
        if context.area.spaces.active.type == 'NODE_EDITOR':
            bpy.ops.bis.get_node_from_storage(nodeGroupId = int(self.items))
        elif context.area.spaces.active.type == 'TEXT_EDITOR':
            bpy.ops.bis.get_text_from_storage(textId = int(self.items))

def register():
    BIS_Items.register()

def unregister():
    BIS_Items.unregister()
