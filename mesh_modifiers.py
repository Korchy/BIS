# Nikita Akimov
# interplanety@interplanety.org

# Mesh Modifiers

from .BLTypesConversion import BLset,BLObject, BLCacheFile, BLVector, BLImage, BLbpy_prop_collection, BLbpy_prop_array, BLCurveMapping, BLTexture


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


class MeshModifierDATA_TRANSFER(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['object'] = BLObject.to_json(instance=modifier.object)
        modifier_json['use_poly_data'] = modifier.use_poly_data
        modifier_json['use_vert_data'] = modifier.use_vert_data
        modifier_json['use_edge_data'] = modifier.use_edge_data
        modifier_json['use_loop_data'] = modifier.use_loop_data
        modifier_json['data_types_edges'] = BLset.to_json(modifier.data_types_edges)
        modifier_json['data_types_loops'] = BLset.to_json(modifier.data_types_loops)
        modifier_json['data_types_polys'] = BLset.to_json(modifier.data_types_polys)
        modifier_json['data_types_verts'] = BLset.to_json(modifier.data_types_verts)
        modifier_json['edge_mapping'] = modifier.edge_mapping
        modifier_json['invert_vertex_group'] = modifier.invert_vertex_group
        modifier_json['islands_precision'] = modifier.islands_precision
        modifier_json['layers_uv_select_dst'] = modifier.layers_uv_select_dst
        modifier_json['layers_uv_select_src'] = modifier.layers_uv_select_src
        modifier_json['layers_vcol_select_dst'] = modifier.layers_vcol_select_dst
        modifier_json['layers_vcol_select_src'] = modifier.layers_vcol_select_src
        modifier_json['layers_vgroup_select_dst'] = modifier.layers_vgroup_select_dst
        modifier_json['layers_vgroup_select_src'] = modifier.layers_vgroup_select_src
        modifier_json['loop_mapping'] = modifier.loop_mapping
        modifier_json['max_distance'] = modifier.max_distance
        modifier_json['mix_factor'] = modifier.mix_factor
        modifier_json['mix_mode'] = modifier.mix_mode
        modifier_json['poly_mapping'] = modifier.poly_mapping
        modifier_json['ray_radius'] = modifier.ray_radius
        modifier_json['use_max_distance'] = modifier.use_max_distance
        modifier_json['use_object_transform'] = modifier.use_object_transform
        modifier_json['vert_mapping'] = modifier.vert_mapping
        modifier_json['vertex_group'] = modifier.vertex_group

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        BLObject.from_json(instance=modifier, json=modifier_json['object'])
        modifier.use_poly_data = modifier_json['use_poly_data']
        modifier.use_vert_data = modifier_json['use_vert_data']
        modifier.use_edge_data = modifier_json['use_edge_data']
        modifier.use_loop_data = modifier_json['use_loop_data']
        modifier.use_max_distance = modifier_json['use_max_distance']
        modifier.use_object_transform = modifier_json['use_object_transform']
        modifier.data_types_edges = BLset.from_json(json=modifier_json['data_types_edges'])
        modifier.data_types_loops = BLset.from_json(json=modifier_json['data_types_loops'])
        modifier.data_types_polys = BLset.from_json(json=modifier_json['data_types_polys'])
        modifier.data_types_verts = BLset.from_json(json=modifier_json['data_types_verts'])
        modifier.edge_mapping = modifier_json['edge_mapping']
        modifier.invert_vertex_group = modifier_json['invert_vertex_group']
        modifier.islands_precision = modifier_json['islands_precision']
        modifier.layers_uv_select_dst = modifier_json['layers_uv_select_dst']
        modifier.layers_uv_select_src = modifier_json['layers_uv_select_src']
        modifier.layers_vcol_select_dst = modifier_json['layers_vcol_select_dst']
        modifier.layers_vcol_select_src = modifier_json['layers_vcol_select_src']
        modifier.layers_vgroup_select_dst = modifier_json['layers_vgroup_select_dst']
        modifier.layers_vgroup_select_src = modifier_json['layers_vgroup_select_src']
        modifier.loop_mapping = modifier_json['loop_mapping']
        modifier.max_distance = modifier_json['max_distance']
        modifier.mix_factor = modifier_json['mix_factor']
        modifier.mix_mode = modifier_json['mix_mode']
        modifier.poly_mapping = modifier_json['poly_mapping']
        modifier.ray_radius = modifier_json['ray_radius']
        modifier.vert_mapping = modifier_json['vert_mapping']
        modifier.vertex_group = modifier_json['vertex_group']


class MeshModifierMESH_CACHE(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['cache_format'] = modifier.cache_format
        modifier_json['deform_mode'] = modifier.deform_mode
        modifier_json['eval_factor'] = modifier.eval_factor
        modifier_json['eval_frame'] = modifier.eval_frame
        modifier_json['eval_time'] = modifier.eval_time
        modifier_json['factor'] = modifier.factor
        modifier_json['filepath'] = modifier.filepath
        modifier_json['flip_axis'] = BLset.to_json(modifier.flip_axis)
        modifier_json['forward_axis'] = modifier.forward_axis
        modifier_json['frame_scale'] = modifier.frame_scale
        modifier_json['frame_start'] = modifier.frame_start
        modifier_json['interpolation'] = modifier.interpolation
        modifier_json['play_mode'] = modifier.play_mode
        modifier_json['time_mode'] = modifier.time_mode
        modifier_json['up_axis'] = modifier.up_axis

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.cache_format = modifier_json['cache_format']
        modifier.deform_mode = modifier_json['deform_mode']
        modifier.eval_factor = modifier_json['eval_factor']
        modifier.eval_frame = modifier_json['eval_frame']
        modifier.eval_time = modifier_json['eval_time']
        modifier.factor = modifier_json['factor']
        modifier.filepath = modifier_json['filepath']
        modifier.flip_axis = BLset.from_json(json=modifier_json['flip_axis'])
        modifier.forward_axis = modifier_json['forward_axis']
        modifier.frame_scale = modifier_json['frame_scale']
        modifier.frame_start = modifier_json['frame_start']
        modifier.interpolation = modifier_json['interpolation']
        modifier.play_mode = modifier_json['play_mode']
        modifier.time_mode = modifier_json['time_mode']
        modifier.up_axis = modifier_json['up_axis']


class MeshModifierMESH_SEQUENCE_CACHE(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['cache_file'] = BLCacheFile.to_json(instance=modifier.cache_file)
        modifier_json['object_path'] = modifier.object_path
        modifier_json['read_data'] = BLset.to_json(modifier.read_data)

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        BLCacheFile.from_json(instance=modifier, json=modifier_json['cache_file'], instance_field='cache_file')
        modifier.object_path = modifier_json['object_path']
        modifier.read_data = BLset.from_json(json=modifier_json['read_data'])


class MeshModifierNORMAL_EDIT(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['target'] = BLObject.to_json(instance=modifier.target)
        modifier_json['invert_vertex_group'] = modifier.invert_vertex_group
        modifier_json['mix_factor'] = modifier.mix_factor
        modifier_json['mix_limit'] = modifier.mix_limit
        modifier_json['mix_mode'] = modifier.mix_mode
        modifier_json['mode'] = modifier.mode
        modifier_json['offset'] = BLVector.to_json(instance=modifier.offset)
        modifier_json['use_direction_parallel'] = modifier.use_direction_parallel
        modifier_json['vertex_group'] = modifier.vertex_group

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        BLObject.from_json(instance=modifier, json=modifier_json['target'], instance_field='target')
        modifier.invert_vertex_group = modifier_json['invert_vertex_group']
        modifier.mix_factor = modifier_json['mix_factor']
        modifier.mix_limit = modifier_json['mix_limit']
        modifier.mix_mode = modifier_json['mix_mode']
        modifier.mode = modifier_json['mode']
        BLVector.from_json(instance=modifier.offset, json=modifier_json['offset'])
        modifier.use_direction_parallel = modifier_json['use_direction_parallel']
        modifier.vertex_group = modifier_json['vertex_group']


class MeshModifierUV_PROJECT(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['aspect_x'] = modifier.aspect_x
        modifier_json['aspect_y'] = modifier.aspect_y
        modifier_json['image'] = BLImage.to_json(instance=modifier.image)
        modifier_json['projector_count'] = modifier.projector_count
        modifier_json['projectors'] = BLbpy_prop_collection.to_json(modifier.projectors)
        modifier_json['scale_x'] = modifier.scale_x
        modifier_json['scale_y'] = modifier.scale_y
        modifier_json['use_image_override'] = modifier.use_image_override
        modifier_json['uv_layer'] = modifier.uv_layer

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.aspect_x = modifier_json['aspect_x']
        modifier.aspect_y = modifier_json['aspect_y']
        BLImage.from_json(instance=modifier, json=modifier_json['image'], instance_field='image')
        modifier.projector_count = modifier_json['projector_count']
        BLbpy_prop_collection.from_json(modifier, modifier.projectors, modifier_json['projectors'])
        modifier.scale_x = modifier_json['scale_x']
        modifier.scale_y = modifier_json['scale_y']
        modifier.use_image_override = modifier_json['use_image_override']
        modifier.uv_layer = modifier_json['uv_layer']


class MeshModifierUV_WARP(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['axis_u'] = modifier.axis_u
        modifier_json['axis_v'] = modifier.axis_v
        modifier_json['bone_from'] = modifier.bone_from
        modifier_json['bone_to'] = modifier.bone_to
        modifier_json['center'] = BLbpy_prop_array.to_json(prop_array=modifier.center)
        modifier_json['object_from'] = BLObject.to_json(instance=modifier.object_from)
        modifier_json['object_to'] = BLObject.to_json(instance=modifier.object_to)
        modifier_json['uv_layer'] = modifier.uv_layer
        modifier_json['vertex_group'] = modifier.vertex_group

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.axis_u = modifier_json['axis_u']
        modifier.axis_v = modifier_json['axis_v']
        modifier.bone_from = modifier_json['bone_from']
        modifier.bone_to = modifier_json['bone_to']
        BLbpy_prop_array.from_json(prop_array=modifier.center, json=modifier_json['center'])
        BLObject.from_json(instance=modifier, json=modifier_json['object_from'], instance_field='object_from')
        BLObject.from_json(instance=modifier, json=modifier_json['object_to'], instance_field='object_to')
        modifier.uv_layer = modifier_json['uv_layer']
        modifier.vertex_group = modifier_json['vertex_group']


class MeshModifierVERTEX_WEIGHT_EDIT(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['add_threshold'] = modifier.add_threshold
        modifier_json['default_weight'] = modifier.default_weight
        modifier_json['falloff_type'] = modifier.falloff_type
        modifier_json['map_curve'] = BLCurveMapping.to_json(instance=modifier.map_curve)
        modifier_json['mask_constant'] = modifier.mask_constant
        modifier_json['mask_tex_map_object'] = BLObject.to_json(instance=modifier.mask_tex_map_object)
        modifier_json['mask_tex_mapping'] = modifier.mask_tex_mapping
        modifier_json['mask_tex_use_channel'] = modifier.mask_tex_use_channel
        modifier_json['mask_tex_uv_layer'] = modifier.mask_tex_uv_layer
        modifier_json['mask_texture'] = BLTexture.to_json(instance=modifier.mask_texture)
        modifier_json['mask_vertex_group'] = modifier.mask_vertex_group
        modifier_json['remove_threshold'] = modifier.remove_threshold
        modifier_json['use_add'] = modifier.use_add
        modifier_json['use_remove'] = modifier.use_remove
        modifier_json['vertex_group'] = modifier.vertex_group

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.add_threshold = modifier_json['add_threshold']
        modifier.default_weight = modifier_json['default_weight']
        modifier.falloff_type = modifier_json['falloff_type']
        BLCurveMapping.from_json(instance=modifier.map_curve, json=modifier_json['map_curve'])
        modifier.mask_constant = modifier_json['mask_constant']
        BLObject.from_json(instance=modifier, json=modifier_json['mask_tex_map_object'], instance_field='mask_tex_map_object')
        modifier.mask_tex_mapping = modifier_json['mask_tex_mapping']
        modifier.mask_tex_use_channel = modifier_json['mask_tex_use_channel']
        modifier.mask_tex_uv_layer = modifier_json['mask_tex_uv_layer']
        BLTexture.from_json(instance=modifier, json=modifier_json['mask_texture'], instance_field='mask_texture')
        modifier.mask_vertex_group = modifier_json['mask_vertex_group']
        modifier.remove_threshold = modifier_json['remove_threshold']
        modifier.use_add = modifier_json['use_add']
        modifier.use_remove = modifier_json['use_remove']
        modifier.vertex_group = modifier_json['vertex_group']
