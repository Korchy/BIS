# Nikita Akimov
# interplanety@interplanety.org

from .JsonEx import JsonEx
from .NodeBase import GIOCommon


class GIONodeSocketColor(GIOCommon):
    @staticmethod
    def gio_to_json(io, gio=None):
        gio_json = super(__class__, __class__).gio_to_json(io, gio)
        gio_json['default_value'] = JsonEx.prop_array_to_json(io.default_value)
        if gio:
            gio_json['value'] = JsonEx.prop_array_to_json(gio.default_value)
        return gio_json
    
    @staticmethod
    def json_to_gi(node_tree, group_node, input_number, input_in_json):
        current_input = super(__class__, __class__).json_to_gi(node_tree, group_node, input_number, input_in_json)
        JsonEx.prop_array_from_json(current_input.default_value, input_in_json['default_value'])
        if input_in_json['value']:
            JsonEx.prop_array_from_json(group_node.inputs[input_number].default_value, input_in_json['value'])
        return current_input
    
    @staticmethod
    def json_to_go(node_tree, output_in_json):
        current_output = super(__class__, __class__).json_to_go(node_tree, output_in_json)
        JsonEx.prop_array_from_json(current_output.default_value, output_in_json['default_value'])
        return current_output


class GIONodeSocketVector(GIONodeSocketColor):
    pass


class GIONodeSocketVectorDirection(GIONodeSocketVector):
    pass


class GIONodeSocketVectorXYZ(GIONodeSocketVector):
    pass


class GIONodeSocketVectorTranslation(GIONodeSocketVector):
    pass


class GIONodeSocketVectorVelocity(GIONodeSocketVector):
    pass


class GIONodeSocketShader(GIOCommon):
    pass


class GIONodeSocketFloat(GIOCommon):
    @staticmethod
    def gio_to_json(io, gio=None):
        gio_json = super(__class__, __class__).gio_to_json(io, gio)
        gio_json['default_value'] = io.default_value
        gio_json['min_value'] = io.min_value
        gio_json['max_value'] = io.max_value
        if gio:
            gio_json['value'] = gio.default_value
        return gio_json

    @staticmethod
    def json_to_gi(node_tree, group_node, input_number, input_in_json):
        current_input = super(__class__, __class__).json_to_gi(node_tree, group_node, input_number, input_in_json)
        current_input.default_value = input_in_json['default_value']
        current_input.min_value = input_in_json['min_value']
        current_input.max_value = input_in_json['max_value']
        group_node.inputs[input_number].default_value = input_in_json['value']
        return current_input

    @staticmethod
    def json_to_go(node_tree, output_in_json):
        current_output = super(__class__, __class__).json_to_go(node_tree, output_in_json)
        current_output.default_value = output_in_json['default_value']
        return current_output


class GIONodeSocketFloatFactor(GIONodeSocketFloat):
    pass


class GIONodeSocketFloatAngle(GIONodeSocketFloat):
    pass


class GIONodeSocketFloatUnsigned(GIONodeSocketFloat):
    pass


class GIONodeSocketInt(GIONodeSocketFloat):
    pass
