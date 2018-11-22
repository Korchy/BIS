# Nikita Akimov
# interplanety@interplanety.org

from .JsonEx import JsonEx


class NodeIOCommon:
    @classmethod
    def io_to_json(cls, io):
        io_json = {
            'type': io.type,
            'bl_idname': io.bl_idname,
            'identifier': io.identifier,
            'name': io.name
        }
        # for current io specification
        cls._io_to_json_spec(io_json, io)
        return io_json

    @classmethod
    def _io_to_json_spec(cls, io_json, io):
        # extend to current io data
        pass

    @classmethod
    def json_to_i(cls, node, node_input, input_json):
        if node_input:
            node_input.name = input_json['name']
            if node_input.bl_idname == input_json['bl_idname']:
                # for current input specification
                cls._json_to_i_spec(node, node_input, input_json)

    @classmethod
    def _json_to_i_spec(cls, node, node_input, input_json):
        # extend to current input data
        pass

    @classmethod
    def json_to_o(cls, node, node_output, output_json):
        if node_output:
            node_output.name = output_json['name']
            if node_output.bl_idname == output_json['bl_idname']:
                # for current output specification
                cls._json_to_o_spec(node, node_output, output_json)

    @classmethod
    def _json_to_o_spec(cls, node, node_output, output_json):
        # extend to current output data
        pass


class NodeIONodeSocketColor(NodeIOCommon):
    @classmethod
    def _io_to_json_spec(cls, io_json, io):
        io_json['default_value'] = JsonEx.prop_array_to_json(io.default_value)

    @classmethod
    def _json_to_i_spec(cls, node, node_input, input_json):
        JsonEx.prop_array_from_json(node_input.default_value, input_json['default_value'])
        if node.type == 'GROUP':
            JsonEx.prop_array_from_json(node.inputs[-1].default_value, input_json['default_value'])

    @classmethod
    def _json_to_o_spec(cls, node, node_output, output_json):
        JsonEx.prop_array_from_json(node_output.default_value, output_json['default_value'])


class NodeIONodeSocketVector(NodeIONodeSocketColor):
    pass


class NodeIONodeSocketVectorDirection(NodeIONodeSocketVector):
    pass


class NodeIONodeSocketVectorXYZ(NodeIONodeSocketVector):
    pass


class NodeIONodeSocketVectorTranslation(NodeIONodeSocketVector):
    pass


class NodeIONodeSocketVectorVelocity(NodeIONodeSocketVector):
    pass


class NodeIONodeSocketShader(NodeIOCommon):
    pass


class NodeIONodeSocketVirtual(NodeIOCommon):
    pass


class NodeIONodeSocketFloat(NodeIOCommon):
    @classmethod
    def _io_to_json_spec(cls, io_json, io):
        io_json['default_value'] = io.default_value

    @classmethod
    def _json_to_i_spec(cls, node, node_input, input_json):
        node_input.default_value = input_json['default_value']
        if node.type == 'GROUP':
            node.inputs[-1].default_value = input_json['default_value']

    @classmethod
    def _json_to_o_spec(cls, node, node_output, output_json):
        node_output.default_value = output_json['default_value']


class NodeIONodeSocketFloatFactor(NodeIONodeSocketFloat):
    pass


class NodeIONodeSocketFloatAngle(NodeIONodeSocketFloat):
    pass


class NodeIONodeSocketFloatUnsigned(NodeIONodeSocketFloat):
    pass


class NodeIONodeSocketInt(NodeIONodeSocketFloat):
    pass


class NodeIONodeGroupInput(NodeIOCommon):
    pass


class NodeIONodeGroupOutput(NodeIONodeGroupInput):
    pass
