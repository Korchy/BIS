# Nikita Akimov
# interplanety@interplanety.org


class NodesTools:

    @staticmethod
    def active_node(context):
        # returns currently active node in NODE_EDITOR window
        selected_node = None
        if context.active_object \
                and context.active_object.active_material \
                and hasattr(context.space_data, 'path'):
            selected_node = context.active_object.active_material.node_tree.nodes.active
            for i in range(len(context.space_data.path) - 1):
                selected_node = selected_node.node_tree.nodes.active
        return selected_node

    @staticmethod
    def add_input_to_node(node, input_type, input_name):
        # add input to node
        if node.node_tree:
            node.node_tree.inputs.new(input_type, input_name)

    @staticmethod
    def add_output_to_node(node, output_type, output_name):
        # add output to node
        if node.node_tree:
            node.node_tree.outputs.new(output_type, output_name)
