# Nikita Akimov
# interplanety@interplanety.org

# Mesh Modifiers


class ModifierCommon:
    @classmethod
    def to_json(cls, modifier):
        # base specification
        modifier_json = {
            'type': modifier.type,
            'name': modifier.name
        }
        # for current specifications
        cls._to_json_spec(modifier_json, modifier)
        return modifier_json

    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        # extend to current modifier data
        pass

    @classmethod
    def from_json(cls, mesh, modifier_json):
        # for current specifications
        mesh.modifiers.new(modifier_json['name'], modifier_json['type'])
        cls._from_json_spec(mesh, modifier_json)
        return mesh

    @classmethod
    def _from_json_spec(cls, mesh, modifier_json):
        # extend to current modifier data
        pass
