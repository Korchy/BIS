bl_info = {
    'name': 'BIS',
    'category': 'Material',
    'author': 'Nikita Akimov',
    'version': (0, 0, 1),
    'blender': (2, 78, 0),
    'location': 'T-Panel > BIS',
    'wiki_url': 'http://b3d.interplanety.ru/bis/',
    'tracker_url': 'http://b3d.interplanety.ru/bis/',
    'description': 'BIS - Blender Interplanety Storage'
}

import sys
import importlib

modulesNames = ['BIS_addNodeToStorage', 'BIS_getNodeFromStorage', 'BIS_getNodesFromStorage', 'WebRequests',
                'BIS_nodesPanel', 'BIS_textsPanel', 'MessageBox', 'NodeManager', 'JsonEx']

modulesFullNames = {}
for currentModuleName in modulesNames:
    if 'DEBUG_MODE' in sys.argv:
        modulesFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))

for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

if __name__ == "__main__":
    register()
