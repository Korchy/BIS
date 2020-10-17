# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

# NodeGroup class

from . import cfg
from .node import Node


class NodeGroup:

    @classmethod
    def to_json(cls, node_group):
        # base node_group specification
        node_group_json = Node.to_json(node=node_group)
        node_group_json['instance']['name'] = node_group.node_tree.name
        node_group_json['instance']['type'] = node_group.type
        return node_group_json

    @classmethod
    def from_json(cls, node_group_json, parent_node_tree, attachments_path):
        node_group = None
        try:
            node_group = parent_node_tree.nodes.new(type=node_group_json['class'])
        except Exception as exception:
            if cfg.show_debug_err:
                print(repr(exception))
        if node_group:
            Node.from_json(
                node=node_group,
                node_json=node_group_json,
                attachments_path=attachments_path
            )
        return node_group
