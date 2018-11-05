# Nikita Akimov
# interplanety@interplanety.org

bl_info = {
    'name': 'BIS',
    'category': 'Material',
    'author': 'Nikita Akimov',
    'version': (1, 4, 0),
    'blender': (2, 79, 0),
    'location': 'T-Panel > BIS',
    'wiki_url': 'https://b3d.interplanety.org/en/bis-online-blender-material-storage/',
    'tracker_url': 'https://b3d.interplanety.org/en/bis-online-blender-material-storage/',
    'description': 'BIS - Blender Interplanety Storage'
}

from . import BIS_addNodeToStorage
from . import BISUpdateNodegroup
from . import BIS_getNodeFromStorage
from . import BIS_getNodesFromStorage
from . import nodes_panel
from . import BIS_addTextToStorage
from . import BISUpdateText
from . import BIS_getTextFromStorage
from . import BIS_getTextsFromStorage
from . import BIS_textsPanel
from . import WebRequests
from . import MessageBox
from . import BIS_Items


def register():
    BIS_addNodeToStorage.register()
    BISUpdateNodegroup.register()
    BIS_getNodeFromStorage.register()
    BIS_getNodesFromStorage.register()
    nodes_panel.register()
    BIS_addTextToStorage.register()
    BISUpdateText.register()
    BIS_getTextFromStorage.register()
    BIS_getTextsFromStorage.register()
    BIS_textsPanel.register()
    WebRequests.register()
    MessageBox.register()
    BIS_Items.register()


def unregister():
    BIS_Items.unregister()
    MessageBox.unregister()
    WebRequests.unregister()
    BIS_textsPanel.unregister()
    BIS_getTextsFromStorage.unregister()
    BIS_getTextFromStorage.unregister()
    BISUpdateText.unregister()
    BIS_addTextToStorage.unregister()
    nodes_panel.unregister()
    BIS_getNodesFromStorage.unregister()
    BIS_getNodeFromStorage.unregister()
    BISUpdateNodegroup.unregister()
    BIS_addNodeToStorage.unregister()


if __name__ == "__main__":
    register()
