# Nikita Akimov
# interplanety@interplanety.org

from . import cfg
from . import add_node_group_to_storage
from . import update_node_group
from . import get_node_group_from_storage
from . import get_nodes_from_storage
from . import nodes_panel
from . import add_text_to_storage
from . import update_text
from . import get_text_from_storage
from . import get_texts_from_storage
from . import texts_panel
from . import mesh_panel
from . import get_meshes_from_storage
from . import add_mesh_to_storage
from . import update_mesh_in_storage
from . import get_mesh_from_storage
from . import WebRequests
from . import message_box
from . import bis_items
from . import nodes_tools_ops
if cfg.experimental_enable_bis_custom_nodes:
    from . import nodes_bis_custom


bl_info = {
    'name': 'BIS',
    'category': 'Material',
    'author': 'Nikita Akimov',
    'version': (1, 6, 3),
    'blender': (2, 80, 0),
    'location': 'N-Panel > BIS',
    'wiki_url': 'https://b3d.interplanety.org/en/bis-online-blender-material-storage/',
    'tracker_url': 'https://b3d.interplanety.org/en/bis-online-blender-material-storage/',
    'description': 'BIS (Blender Interplanety Storage) - online materials/shaders library'
}


def register():
    add_node_group_to_storage.register()
    update_node_group.register()
    get_node_group_from_storage.register()
    get_nodes_from_storage.register()
    nodes_panel.register()
    if cfg.experimental_enable_bis_custom_nodes:
        nodes_bis_custom.register()
    add_text_to_storage.register()
    update_text.register()
    get_text_from_storage.register()
    get_texts_from_storage.register()
    texts_panel.register()
    mesh_panel.register()
    get_meshes_from_storage.register()
    add_mesh_to_storage.register()
    update_mesh_in_storage.register()
    get_mesh_from_storage.register()
    WebRequests.register()
    message_box.register()
    bis_items.register()
    nodes_tools_ops.register()


def unregister():
    nodes_tools_ops.unregister()
    bis_items.unregister()
    message_box.unregister()
    WebRequests.unregister()
    get_mesh_from_storage.unregister()
    update_mesh_in_storage.unregister()
    add_mesh_to_storage.unregister()
    get_meshes_from_storage.unregister()
    mesh_panel.unregister()
    texts_panel.unregister()
    get_texts_from_storage.unregister()
    get_text_from_storage.unregister()
    update_text.unregister()
    add_text_to_storage.unregister()
    if cfg.experimental_enable_bis_custom_nodes:
        nodes_bis_custom.unregister()
    nodes_panel.unregister()
    get_nodes_from_storage.unregister()
    get_node_group_from_storage.unregister()
    update_node_group.unregister()
    add_node_group_to_storage.unregister()


if __name__ == "__main__":
    register()
