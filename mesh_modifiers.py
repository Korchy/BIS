# Nikita Akimov
# interplanety@interplanety.org

# Mesh Modifiers

import os
import bpy
from .BLTypesConversion import BLset, BLObject, BLCacheFile, BLVector, BLImage, BLbpy_prop_collection, BLbpy_prop_array, BLCurveMapping, BLTexture


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


class MeshModifierVERTEX_WEIGHT_MIX(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['default_weight_a'] = modifier.default_weight_a
        modifier_json['default_weight_b'] = modifier.default_weight_b
        modifier_json['mask_constant'] = modifier.mask_constant
        modifier_json['mask_tex_map_object'] = BLObject.to_json(instance=modifier.mask_tex_map_object)
        modifier_json['mask_tex_mapping'] = modifier.mask_tex_mapping
        modifier_json['mask_tex_use_channel'] = modifier.mask_tex_use_channel
        modifier_json['mask_tex_uv_layer'] = modifier.mask_tex_uv_layer
        modifier_json['mask_texture'] = BLTexture.to_json(instance=modifier.mask_texture)
        modifier_json['mask_vertex_group'] = modifier.mask_vertex_group
        modifier_json['mix_mode'] = modifier.mix_mode
        modifier_json['mix_set'] = modifier.mix_set
        modifier_json['vertex_group_a'] = modifier.vertex_group_a

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.default_weight_a = modifier_json['default_weight_a']
        modifier.default_weight_b = modifier_json['default_weight_b']
        modifier.mask_constant = modifier_json['mask_constant']
        BLObject.from_json(instance=modifier, json=modifier_json['mask_tex_map_object'], instance_field='mask_tex_map_object')
        modifier.mask_tex_mapping = modifier_json['mask_tex_mapping']
        modifier.mask_tex_use_channel = modifier_json['mask_tex_use_channel']
        modifier.mask_tex_uv_layer = modifier_json['mask_tex_uv_layer']
        BLTexture.from_json(instance=modifier, json=modifier_json['mask_texture'], instance_field='mask_texture')
        modifier.mask_vertex_group = modifier_json['mask_vertex_group']
        modifier.mix_mode = modifier_json['mix_mode']
        modifier.mix_set = modifier_json['mix_set']
        modifier.vertex_group_a = modifier_json['vertex_group_a']


class MeshModifierVERTEX_WEIGHT_PROXIMITY(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['falloff_type'] = modifier.falloff_type
        modifier_json['mask_constant'] = modifier.mask_constant
        modifier_json['mask_tex_map_object'] = BLObject.to_json(instance=modifier.mask_tex_map_object)
        modifier_json['mask_tex_mapping'] = modifier.mask_tex_mapping
        modifier_json['mask_tex_use_channel'] = modifier.mask_tex_use_channel
        modifier_json['mask_tex_uv_layer'] = modifier.mask_tex_uv_layer
        modifier_json['mask_texture'] = BLTexture.to_json(instance=modifier.mask_texture)
        modifier_json['mask_vertex_group'] = modifier.mask_vertex_group
        modifier_json['max_dist'] = modifier.max_dist
        modifier_json['min_dist'] = modifier.min_dist
        modifier_json['proximity_geometry'] = BLset.to_json(modifier.proximity_geometry)
        modifier_json['proximity_mode'] = modifier.proximity_mode
        modifier_json['target'] = BLObject.to_json(instance=modifier.target)
        modifier_json['vertex_group'] = modifier.vertex_group

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.falloff_type = modifier_json['falloff_type']
        modifier.mask_constant = modifier_json['mask_constant']
        BLObject.from_json(instance=modifier, json=modifier_json['mask_tex_map_object'], instance_field='mask_tex_map_object')
        modifier.mask_tex_mapping = modifier_json['mask_tex_mapping']
        modifier.mask_tex_use_channel = modifier_json['mask_tex_use_channel']
        modifier.mask_tex_uv_layer = modifier_json['mask_tex_uv_layer']
        BLTexture.from_json(instance=modifier, json=modifier_json['mask_texture'], instance_field='mask_texture')
        modifier.mask_vertex_group = modifier_json['mask_vertex_group']
        modifier.max_dist = modifier_json['max_dist']
        modifier.min_dist = modifier_json['min_dist']
        modifier.proximity_geometry = BLset.from_json(json=modifier_json['proximity_geometry'])
        modifier.proximity_mode = modifier_json['proximity_mode']
        BLObject.from_json(instance=modifier, json=modifier_json['target'], instance_field='target')
        modifier.vertex_group = modifier_json['vertex_group']


class MeshModifierARRAY(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['constant_offset_displace'] = BLVector.to_json(instance=modifier.constant_offset_displace)
        modifier_json['count'] = modifier.count
        modifier_json['curve'] = BLObject.to_json(instance=modifier.curve)
        modifier_json['end_cap'] = BLObject.to_json(instance=modifier.end_cap)
        modifier_json['start_cap'] = BLObject.to_json(instance=modifier.start_cap)
        modifier_json['offset_object'] = BLObject.to_json(instance=modifier.offset_object)
        modifier_json['fit_length'] = modifier.fit_length
        modifier_json['fit_type'] = modifier.fit_type
        modifier_json['merge_threshold'] = modifier.merge_threshold
        modifier_json['relative_offset_displace'] = BLbpy_prop_array.to_json(prop_array=modifier.relative_offset_displace)
        modifier_json['use_constant_offset'] = modifier.use_constant_offset
        modifier_json['use_merge_vertices'] = modifier.use_merge_vertices
        modifier_json['use_merge_vertices_cap'] = modifier.use_merge_vertices_cap
        modifier_json['use_object_offset'] = modifier.use_object_offset
        modifier_json['use_relative_offset'] = modifier.use_relative_offset

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        BLVector.from_json(instance=modifier.constant_offset_displace, json=modifier_json['constant_offset_displace'])
        modifier.count = modifier_json['count']
        BLObject.from_json(instance=modifier, json=modifier_json['curve'], instance_field='curve')
        BLObject.from_json(instance=modifier, json=modifier_json['end_cap'], instance_field='end_cap')
        BLObject.from_json(instance=modifier, json=modifier_json['start_cap'], instance_field='start_cap')
        BLObject.from_json(instance=modifier, json=modifier_json['offset_object'], instance_field='offset_object')
        modifier.fit_length = modifier_json['fit_length']
        modifier.fit_type = modifier_json['fit_type']
        modifier.merge_threshold = modifier_json['merge_threshold']
        BLbpy_prop_array.from_json(prop_array=modifier.relative_offset_displace, json=modifier_json['relative_offset_displace'])
        modifier.use_constant_offset = modifier_json['use_constant_offset']
        modifier.use_merge_vertices = modifier_json['use_merge_vertices']
        modifier.use_merge_vertices_cap = modifier_json['use_merge_vertices_cap']
        modifier.use_object_offset = modifier_json['use_object_offset']
        modifier.use_relative_offset = modifier_json['use_relative_offset']


class MeshModifierBEVEL(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['angle_limit'] = modifier.angle_limit
        modifier_json['edge_weight_method'] = modifier.edge_weight_method
        modifier_json['limit_method'] = modifier.limit_method
        modifier_json['loop_slide'] = modifier.loop_slide
        modifier_json['material'] = modifier.material
        modifier_json['offset_type'] = modifier.offset_type
        modifier_json['profile'] = modifier.profile
        modifier_json['segments'] = modifier.segments
        modifier_json['use_clamp_overlap'] = modifier.use_clamp_overlap
        modifier_json['use_only_vertices'] = modifier.use_only_vertices
        modifier_json['vertex_group'] = modifier.vertex_group
        modifier_json['width'] = modifier.width

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.angle_limit = modifier_json['angle_limit']
        modifier.edge_weight_method = modifier_json['edge_weight_method']
        modifier.limit_method = modifier_json['limit_method']
        modifier.loop_slide = modifier_json['loop_slide']
        modifier.material = modifier_json['material']
        modifier.offset_type = modifier_json['offset_type']
        modifier.profile = modifier_json['profile']
        modifier.segments = modifier_json['segments']
        modifier.use_clamp_overlap = modifier_json['use_clamp_overlap']
        modifier.use_only_vertices = modifier_json['use_only_vertices']
        modifier.vertex_group = modifier_json['vertex_group']
        modifier.width = modifier_json['width']


class MeshModifierBOOLEAN(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['debug_options'] = BLset.to_json(modifier.debug_options)
        modifier_json['double_threshold'] = modifier.double_threshold
        modifier_json['object'] = BLObject.to_json(instance=modifier.object)
        modifier_json['operation'] = modifier.operation
        modifier_json['solver'] = modifier.solver

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.debug_options = BLset.from_json(json=modifier_json['debug_options'])
        modifier.double_threshold = modifier_json['double_threshold']
        BLObject.from_json(instance=modifier, json=modifier_json['object'], instance_field='object')
        modifier.operation = modifier_json['operation']
        modifier.solver = modifier_json['solver']


class MeshModifierBUILD(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['frame_duration'] = modifier.frame_duration
        modifier_json['frame_start'] = modifier.frame_start
        modifier_json['seed'] = modifier.seed
        modifier_json['use_random_order'] = modifier.use_random_order
        modifier_json['use_reverse'] = modifier.use_reverse

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.frame_duration = modifier_json['frame_duration']
        modifier.frame_start = modifier_json['frame_start']
        modifier.seed = modifier_json['seed']
        modifier.use_random_order = modifier_json['use_random_order']
        modifier.use_reverse = modifier_json['use_reverse']


class MeshModifierDECIMATE(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['angle_limit'] = modifier.angle_limit
        modifier_json['decimate_type'] = modifier.decimate_type
        modifier_json['delimit'] = BLset.to_json(modifier.delimit)
        modifier_json['invert_vertex_group'] = modifier.invert_vertex_group
        modifier_json['iterations'] = modifier.iterations
        modifier_json['ratio'] = modifier.ratio
        modifier_json['symmetry_axis'] = modifier.symmetry_axis
        modifier_json['use_collapse_triangulate'] = modifier.use_collapse_triangulate
        modifier_json['use_dissolve_boundaries'] = modifier.use_dissolve_boundaries
        modifier_json['use_symmetry'] = modifier.use_symmetry
        modifier_json['vertex_group'] = modifier.vertex_group
        modifier_json['vertex_group_factor'] = modifier.vertex_group_factor

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.angle_limit = modifier_json['angle_limit']
        modifier.decimate_type = modifier_json['decimate_type']
        modifier.delimit = BLset.from_json(json=modifier_json['delimit'])
        modifier.invert_vertex_group = modifier_json['invert_vertex_group']
        modifier.iterations = modifier_json['iterations']
        modifier.ratio = modifier_json['ratio']
        modifier.symmetry_axis = modifier_json['symmetry_axis']
        modifier.use_collapse_triangulate = modifier_json['use_collapse_triangulate']
        modifier.use_dissolve_boundaries = modifier_json['use_dissolve_boundaries']
        modifier.use_symmetry = modifier_json['use_symmetry']
        modifier.vertex_group = modifier_json['vertex_group']
        modifier.vertex_group_factor = modifier_json['vertex_group_factor']


class MeshModifierEDGE_SPLIT(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['split_angle'] = modifier.split_angle
        modifier_json['use_edge_angle'] = modifier.use_edge_angle
        modifier_json['use_edge_sharp'] = modifier.use_edge_sharp

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.split_angle = modifier_json['split_angle']
        modifier.use_edge_angle = modifier_json['use_edge_angle']
        modifier.use_edge_sharp = modifier_json['use_edge_sharp']


class MeshModifierMASK(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['armature'] = BLObject.to_json(instance=modifier.armature)
        modifier_json['invert_vertex_group'] = modifier.invert_vertex_group
        modifier_json['mode'] = modifier.mode
        modifier_json['vertex_group'] = modifier.vertex_group

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        BLObject.from_json(instance=modifier, json=modifier_json['armature'], instance_field='armature')
        modifier.invert_vertex_group = modifier_json['invert_vertex_group']
        modifier.mode = modifier_json['mode']
        modifier.vertex_group = modifier_json['vertex_group']


class MeshModifierMIRROR(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['mirror_object'] = BLObject.to_json(instance=modifier.mirror_object)
        modifier_json['merge_threshold'] = modifier.merge_threshold
        modifier_json['mirror_offset_u'] = modifier.mirror_offset_u
        modifier_json['mirror_offset_v'] = modifier.mirror_offset_v
        modifier_json['use_clip'] = modifier.use_clip
        modifier_json['use_mirror_merge'] = modifier.use_mirror_merge
        modifier_json['use_mirror_u'] = modifier.use_mirror_u
        modifier_json['use_mirror_v'] = modifier.use_mirror_v
        modifier_json['use_mirror_vertex_groups'] = modifier.use_mirror_vertex_groups
        modifier_json['use_x'] = modifier.use_x
        modifier_json['use_y'] = modifier.use_y
        modifier_json['use_z'] = modifier.use_z

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        BLObject.from_json(instance=modifier, json=modifier_json['mirror_object'], instance_field='mirror_object')
        modifier.merge_threshold = modifier_json['merge_threshold']
        modifier.mirror_offset_u = modifier_json['mirror_offset_u']
        modifier.mirror_offset_v = modifier_json['mirror_offset_v']
        modifier.use_clip = modifier_json['use_clip']
        modifier.use_mirror_merge = modifier_json['use_mirror_merge']
        modifier.use_mirror_u = modifier_json['use_mirror_u']
        modifier.use_mirror_v = modifier_json['use_mirror_v']
        modifier.use_mirror_vertex_groups = modifier_json['use_mirror_vertex_groups']
        modifier.use_x = modifier_json['use_x']
        modifier.use_y = modifier_json['use_y']
        modifier.use_z = modifier_json['use_z']


class MeshModifierMULTIRES(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['filepath'] = os.path.normpath(os.path.join(os.path.dirname(bpy.data.filepath), modifier.filepath.replace('//', '')))
        modifier_json['levels'] = modifier.levels
        modifier_json['render_levels'] = modifier.render_levels
        modifier_json['sculpt_levels'] = modifier.sculpt_levels
        modifier_json['show_only_control_edges'] = modifier.show_only_control_edges
        modifier_json['subdivision_type'] = modifier.subdivision_type
        modifier_json['use_subsurf_uv'] = modifier.use_subsurf_uv

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.filepath = modifier_json['filepath']
        modifier.levels = modifier_json['levels']
        modifier.render_levels = modifier_json['render_levels']
        modifier.sculpt_levels = modifier_json['sculpt_levels']
        modifier.show_only_control_edges = modifier_json['show_only_control_edges']
        modifier.subdivision_type = modifier_json['subdivision_type']
        modifier.use_subsurf_uv = modifier_json['use_subsurf_uv']


class MeshModifierREMESH(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['mode'] = modifier.mode
        modifier_json['octree_depth'] = modifier.octree_depth
        modifier_json['scale'] = modifier.scale
        modifier_json['sharpness'] = modifier.sharpness
        modifier_json['threshold'] = modifier.threshold
        modifier_json['use_remove_disconnected'] = modifier.use_remove_disconnected
        modifier_json['use_smooth_shade'] = modifier.use_smooth_shade

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.mode = modifier_json['mode']
        modifier.octree_depth = modifier_json['octree_depth']
        modifier.scale = modifier_json['scale']
        modifier.sharpness = modifier_json['sharpness']
        modifier.threshold = modifier_json['threshold']
        modifier.use_remove_disconnected = modifier_json['use_remove_disconnected']
        modifier.use_smooth_shade = modifier_json['use_smooth_shade']


class MeshModifierSCREW(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['object'] = BLObject.to_json(instance=modifier.object)
        modifier_json['angle'] = modifier.angle
        modifier_json['axis'] = modifier.axis
        modifier_json['iterations'] = modifier.iterations
        modifier_json['merge_threshold'] = modifier.merge_threshold
        modifier_json['render_steps'] = modifier.render_steps
        modifier_json['screw_offset'] = modifier.screw_offset
        modifier_json['steps'] = modifier.steps
        modifier_json['use_merge_vertices'] = modifier.use_merge_vertices
        modifier_json['use_normal_calculate'] = modifier.use_normal_calculate
        modifier_json['use_normal_flip'] = modifier.use_normal_flip
        modifier_json['use_object_screw_offset'] = modifier.use_object_screw_offset
        modifier_json['use_smooth_shade'] = modifier.use_smooth_shade
        modifier_json['use_stretch_u'] = modifier.use_stretch_u
        modifier_json['use_stretch_v'] = modifier.use_stretch_v

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        BLObject.from_json(instance=modifier, json=modifier_json['object'], instance_field='object')
        modifier.angle = modifier_json['angle']
        modifier.axis = modifier_json['axis']
        modifier.iterations = modifier_json['iterations']
        modifier.merge_threshold = modifier_json['merge_threshold']
        modifier.render_steps = modifier_json['render_steps']
        modifier.screw_offset = modifier_json['screw_offset']
        modifier.steps = modifier_json['steps']
        modifier.use_merge_vertices = modifier_json['use_merge_vertices']
        modifier.use_normal_calculate = modifier_json['use_normal_calculate']
        modifier.use_normal_flip = modifier_json['use_normal_flip']
        modifier.use_object_screw_offset = modifier_json['use_object_screw_offset']
        modifier.use_smooth_shade = modifier_json['use_smooth_shade']
        modifier.use_stretch_u = modifier_json['use_stretch_u']
        modifier.use_stretch_v = modifier_json['use_stretch_v']


class MeshModifierSKIN(MeshModifierCommon):
    @classmethod
    def _to_json_spec(cls, modifier_json, modifier):
        modifier_json['branch_smoothing'] = modifier.branch_smoothing
        modifier_json['use_smooth_shade'] = modifier.use_smooth_shade
        modifier_json['use_x_symmetry'] = modifier.use_x_symmetry
        modifier_json['use_y_symmetry'] = modifier.use_y_symmetry
        modifier_json['use_z_symmetry'] = modifier.use_z_symmetry

    @classmethod
    def _from_json_spec(cls, modifier, modifier_json):
        modifier.branch_smoothing = modifier_json['branch_smoothing']
        modifier.use_smooth_shade = modifier_json['use_smooth_shade']
        modifier.use_x_symmetry = modifier_json['use_x_symmetry']
        modifier.use_y_symmetry = modifier_json['use_y_symmetry']
        modifier.use_z_symmetry = modifier_json['use_z_symmetry']
