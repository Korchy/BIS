# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

class NodesTools:

    @staticmethod
    def add_input_to_node(node, input_type, input_name):
        # add input to node
        if node and node.node_tree:
            node.node_tree.inputs.new(input_type, input_name)

    @staticmethod
    def add_output_to_node(node, output_type, output_name):
        # add output to node
        if node and node.node_tree:
            node.node_tree.outputs.new(output_type, output_name)
