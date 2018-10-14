# Nikita Akimov
# interplanety@interplanety.org

from .JsonEx import JsonEx
from .NodeBase import IOCommon


class IONodeSocketColor(IOCommon):
    @staticmethod
    def io_to_json(io):
        io_json = super(__class__, __class__).io_to_json(io)
        io_json['default_value'] = JsonEx.prop_array_to_json(io.default_value)
        return io_json

    @staticmethod
    def json_to_i(node, input_number, input_in_json):
        super(__class__, __class__).json_to_i(node, input_number, input_in_json)
        JsonEx.prop_array_from_json(node.inputs[input_number].default_value, input_in_json['default_value'])

    @staticmethod
    def json_to_o(node, output_number, output_in_json):
        super(__class__, __class__).json_to_o(node, output_number, output_in_json)
        JsonEx.prop_array_from_json(node.outputs[output_number].default_value, output_in_json['default_value'])


class IONodeSocketVector(IONodeSocketColor):
    pass


class IONodeSocketVectorDirection(IONodeSocketVector):
    pass


class IONodeSocketVectorXYZ(IONodeSocketVector):
    pass


class IONodeSocketVectorTranslation(IONodeSocketVector):
    pass


class IONodeSocketVectorVelocity(IONodeSocketVector):
    pass


class IONodeSocketShader(IOCommon):
    pass


class IONodeSocketVirtual(IOCommon):
    pass


class IONodeSocketFloat(IOCommon):
    @staticmethod
    def io_to_json(io):
        io_json = super(__class__, __class__).io_to_json(io)
        io_json['default_value'] = io.default_value
        return io_json

    @staticmethod
    def json_to_i(node, input_number, input_in_json):
        super(__class__, __class__).json_to_i(node, input_number, input_in_json)
        node.inputs[input_number].default_value = input_in_json['default_value']

    @staticmethod
    def json_to_o(node, output_number, output_in_json):
        super(__class__, __class__).json_to_o(node, output_number, output_in_json)
        node.outputs[output_number].default_value = output_in_json['default_value']


class IONodeSocketFloatFactor(IONodeSocketFloat):
    pass


class IONodeSocketFloatAngle(IONodeSocketFloat):
    pass


class IONodeSocketFloatUnsigned(IONodeSocketFloat):
    pass


class IONodeSocketInt(IONodeSocketFloat):
    pass


class IONodeGroupInput:
    @staticmethod
    def io_to_json(io):
        return {}

    @staticmethod
    def json_to_i(node, input_number, input_in_json):
        pass

    @staticmethod
    def json_to_o(node, output_number, output_in_json):
        pass


class IONodeGroupOutput(IONodeGroupInput):
    pass
