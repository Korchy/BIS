# Nikita Akimov
# interplanety@interplanety.org
#
# GitHub
#   https://github.com/Korchy/BIS

# node class

import bpy
from .bl_types import BlTypes


class Node:

    @classmethod
    def to_json(cls, node):
        # node to json
        node_json = {
            'class': node.__class__.__name__,   # maybe node.bl_idname
            'instance': {
                'inputs': [],
                'outputs': []
            },
            'bis_node_uid': node['bis_node_uid'] if 'bis_node_uid' in node else None
        }
        # node attributes
        # don't process
        excluded_attributes = [
            'dimensions', 'inputs', 'internal_links', 'node_tree', 'outputs', 'rna_type', 'select',
            'shading_compatibility', 'show_options', 'show_preview', 'show_texture', 'width_hidden'
        ]
        # this attributes - complex
        complex_attributes = ['color_ramp', 'mapping']
        # process first - because they influence on other attributes
        preordered_attributes = [
            attr for attr in ['mode', 'parent'] if
            hasattr(node, attr)
            and getattr(node, attr) is not None  # don't add attributes == None
            and not (isinstance(getattr(node, attr), str) and not getattr(node, attr))  # don't add attributes == '' (empty string)
            and (not node.is_property_readonly(attr) or attr in complex_attributes)  # read-only attributes - only complex
        ]
        # get attributes from node
        node_attributes = [
            attr for attr in dir(node) if
            hasattr(node, attr)
            and not attr.startswith('__')
            and not attr.startswith('bl_')
            and attr not in excluded_attributes
            and attr not in preordered_attributes  # don't add preorderd attributes, added first manually
            and not callable(getattr(node, attr))
            and getattr(node, attr) is not None  # don't add attributes == None
            and not (isinstance(getattr(node, attr), str) and not getattr(node, attr))  # don't add attributes == '' (empty string)
            and (not node.is_property_readonly(attr) or attr in complex_attributes)     # read-only attributes - only complex
        ]
        # all attributes: first - preordered attributes, next - all other attributes
        all_attributes = preordered_attributes + node_attributes
        # get json
        for attr in all_attributes:
            node_json['instance'].update(
                BlTypes.to_json(
                    instance=getattr(node, attr),
                    instance_name=attr,
                    attachments_path=None,
                    excluded_attributes=excluded_attributes,
                    first_attributes=preordered_attributes
                )
            )
        # node inputs/outputs
        if node.type not in ['REROUTE']:
            # inputs
            if node.inputs:
                for c_input in node.inputs:
                    if c_input.bl_idname not in ['NodeSocketVirtual']:
                        input_json = BlTypes.to_json(
                            instance=c_input
                        )
                        input_json['identifier'] = c_input.identifier
                        node_json['instance']['inputs'].append(input_json)
            # outputs
            if node.outputs:
                for c_output in node.outputs:
                    if c_output.bl_idname not in ['NodeSocketVirtual']:
                        output_json = BlTypes.to_json(
                            instance=c_output
                        )
                        output_json['identifier'] = c_output.identifier
                        node_json['instance']['outputs'].append(output_json)
        # for node groups - node tree
        if node.type == 'GROUP':
            from .node_tree import NodeTree     # import here to prevent cyclic import
            node_json['instance']['node_tree'] = NodeTree.to_json(node_tree_parent=node, node_tree=node.node_tree)
        # for current node specification
        cls._node_to_json_spec(node_json, node)
        return node_json

    @classmethod
    def _node_to_json_spec(cls, node_json, node):
        # extend to current node data
        pass

    @classmethod
    def from_json(cls, node, node_json, attachments_path):
        if node:
            # bis uid
            node['bis_node_uid'] = node_json['bis_node_uid'] if 'bis_node_uid' in node_json else None
            # node attributes
            # if node = node group - add node tree
            if node.type == 'GROUP':
                tree_type = node_json['instance']['node_tree']['instance']['bl_idname'] if 'bl_idname' in node_json['instance']['node_tree']['instance'] else 'ShaderNodeTree'
                node.node_tree = bpy.data.node_groups.new(type=tree_type, name=node_json['instance']['node_tree']['instance']['name'])
                from .node_tree import NodeTree  # import here to prevent cyclic import
                NodeTree.from_json(
                    node_tree_parent=node,
                    node_tree_json=node_json['instance']['node_tree'],
                    attachments_path=attachments_path,
                    bis_version='1.9.0'
                )
            # don't process
            excluded_attributes = [
                'inputs', 'outputs', 'node_tree', 'type'
            ]
            # first attributes - process first because they influence on other attributes
            first_attributes = [
                attribute_name for attribute_name in node_json['instance'] if
                attribute_name in ['mode', 'parent']
            ]
            for attribute_name in first_attributes:
                if hasattr(node, attribute_name):
                    BlTypes.from_json(
                        instance_name=attribute_name,
                        instance_owner=node,
                        instance_json=node_json['instance'][attribute_name],
                        attachments_path=attachments_path
                    )
            excluded_attributes += first_attributes
            # for all other node attributes
            for attribute_name in node_json['instance']:
                if attribute_name not in excluded_attributes and hasattr(node, attribute_name):
                    # print('attribute', attribute_name)
                    BlTypes.from_json(
                        instance_name=attribute_name,
                        instance_owner=node,
                        instance_json=node_json['instance'][attribute_name],
                        attachments_path=attachments_path
                    )
            # node inputs
            for input_number, input_json in enumerate(node_json['instance']['inputs']):
                if node.type in ['GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT']:
                    # for group inputs/outputs - by number
                    current_input = node.inputs[input_number]
                else:
                    # for other nodes - by identifier
                    current_input = cls.input_by_identifier(node=node, identifier=input_json['identifier'])
                if current_input:
                    BlTypes.complex_from_json(
                        instance=current_input,
                        json=input_json,
                        excluded_attributes=['bl_idname', 'name', 'type']
                    )
            # node outputs
            for output_number, output_json in enumerate(node_json['instance']['outputs']):
                if node.type in ['GROUP', 'GROUP_INPUT', 'GROUP_OUTPUT']:
                    # for group inputs/outputs - by number
                    current_output = node.outputs[output_number]
                else:
                    # for other nodes - by identifier
                    current_output = cls.output_by_identifier(node=node, identifier=output_json['identifier'])
                if current_output:
                    BlTypes.complex_from_json(
                        instance=current_output,
                        json=output_json,
                        excluded_attributes=['bl_idname', 'name', 'type']
                    )
            # for current node specification
            cls._json_to_node_spec(node, node_json, attachments_path)
        return node

    @classmethod
    def _json_to_node_spec(cls, node, node_json, attachments_path):
        # extend to current node data
        pass

    @classmethod
    def input_by_identifier(cls, node, identifier):
        # returns input by its identifier
        rez = None
        if identifier:
            input_with_identifier = [node_input for node_input in node.inputs[:] if node_input.identifier == identifier]
            if input_with_identifier:
                rez = input_with_identifier[0]
        return rez

    @classmethod
    def output_by_identifier(cls, node, identifier):
        # returns output by its identifier
        rez = None
        if identifier:
            output_with_identifier = [node_output for node_output in node.outputs[:] if node_output.identifier == identifier]
            if output_with_identifier:
                rez = output_with_identifier[0]
        return rez
