# Nikita Akimov
# interplanety@interplanety.org

# Mesh Modifiers


class MeshModifierCommon:
    @classmethod
    def to_json(cls, modifier):
        # base specification
        modifier_json = {
            'type': modifier.type,
            'name': modifier.name,
            'show_expanded': modifier.show_expanded,
            'show_render': modifier.show_render,
            'show_viewport': modifier.show_viewport,
            'show_in_editmode': modifier.show_in_editmode,
            'show_on_cage': modifier.show_on_cage,
            'use_apply_on_spline': modifier.use_apply_on_spline
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
        modifier = mesh.modifiers.new(modifier_json['name'], modifier_json['type'])
        modifier.show_expanded = modifier_json['show_expanded']
        modifier.show_render = modifier_json['show_render']
        modifier.show_viewport = modifier_json['show_viewport']
        modifier.show_in_editmode = modifier_json['show_in_editmode']
        modifier.show_on_cage = modifier_json['show_on_cage']
        modifier.use_apply_on_spline = modifier_json['use_apply_on_spline']
        cls._from_json_spec(modifier=modifier, modifier_json=modifier_json)
        return mesh

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        # extend to current modifier data
        pass


class MeshModifierSUBSURF(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['levels'] = modifier.levels
        modifier_json['render_levels'] = modifier.render_levels
        modifier_json['show_only_control_edges'] = modifier.show_only_control_edges
        modifier_json['subdivision_type'] = modifier.subdivision_type
        modifier_json['use_opensubdiv'] = modifier.use_opensubdiv
        modifier_json['use_subsurf_uv'] = modifier.use_subsurf_uv

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.levels = modifier_json['levels']
        modifier.render_levels = modifier_json['render_levels']
        modifier.show_only_control_edges = modifier_json['show_only_control_edges']
        modifier.subdivision_type = modifier_json['subdivision_type']
        modifier.use_opensubdiv = modifier_json['use_opensubdiv']
        modifier.use_subsurf_uv = modifier_json['use_subsurf_uv']
