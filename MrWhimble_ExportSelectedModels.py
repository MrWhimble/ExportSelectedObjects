import bpy
import os

bl_info = \
{
    "name" : "Export Selected Models",
    "author" : "MrWhimble",
    "version" : (1, 0, 0),
    "blender" : (3, 5, 0),
    "location" : "Tools",
    "description" : "Moves all selected models to the origin, exports them individually with the model's name using preferences made for Unity, and moves the models back to their original positions",
    "warning" : "Might break something, idk",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "Import-Export"
}

def mrwhimble_move_models_to_origin():
    # Store original positions
    original_transforms = []
    for obj in bpy.context.selected_objects:
        original_transforms.append((obj, obj.location.copy(), obj.rotation_euler.copy()))

    # Move models to origin
    #bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    for obj in bpy.context.selected_objects:
        obj.location = (0, 0, 0)
        obj.rotation_euler = (0, 0, 0)

    return original_transforms


def mrwhimble_move_models_to_original_positions(original_transforms):
    # Move models back to their original positions
    for obj, original_position, original_rotation_euler in original_transforms:
        obj.location = original_position
        obj.rotation_euler = original_rotation_euler


def mrwhimble_export_models_fbx(export_path):
    # Get the selected objects
    selected_objects = bpy.context.selected_objects

    # Deselect all objects
    for obj in selected_objects:
        obj.select_set(False)

    # Export each selected object as FBX
    for obj in selected_objects:
        # select current object
        obj.select_set(True)
        
        # Set the export path and filename
        export_filename = bpy.path.clean_name(obj.name) + ".fbx"
        export_filepath = os.path.join(export_path, export_filename)
        # Set custom export settings
        bpy.ops.export_scene.fbx(
            filepath=export_filepath, # File Path
            check_existing=False, # Check Existing
            filter_glob='*.fbx', # File Suffix
            use_selection=True, # Selected Objects
            use_visible=False, # Visible Objects
            use_active_collection=False, # Active Collection
            global_scale=1.0, # Scale
            apply_unit_scale=True, # Apply Unit
            apply_scale_options='FBX_SCALE_UNITS', # Apply Scaling
            use_space_transform=True, # Use Space Transform
            bake_space_transform=True, # Apply Transform
            object_types={'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}, # Object Types
            use_mesh_modifiers=True, # Apply Modifiers
            use_mesh_modifiers_render=False, # Apply Modifiers (Render)
            mesh_smooth_type='OFF', # Smoothing
            colors_type='SRGB', # Vertex Colors
            prioritize_active_color=False, # Prioritize Active Color
            use_subsurf=False, # Export Subdivision Surface
            use_mesh_edges=False, # Loose Edges
            use_tspace=False, # Tangent Space
            use_triangles=False, # Triangulate Faces
            use_custom_props=False, # Custom Properties
            add_leaf_bones=False, # Add Leaf Bones
            primary_bone_axis='Z', # Primary Bone Axis
            secondary_bone_axis='X', # Secondary Bone Axis
            use_armature_deform_only=False, # Only Deform Bones
            armature_nodetype='NULL', # Armature FBXNode Type
            bake_anim=True, # Bake Animation
            bake_anim_use_all_bones=True, # Key All Bones
            bake_anim_use_nla_strips=True, # NLA Strips
            bake_anim_use_all_actions=True, # All Actions
            bake_anim_force_startend_keying=True, # Force Start/End Keying
            bake_anim_step=1.0, # Sampling Rate
            bake_anim_simplify_factor=1.0, # Simplify
            path_mode='AUTO', # Path Mode
            embed_textures=False, # Embed Textures
            batch_mode='OFF', # Batch Mode
            use_batch_own_dir=True, # Batch Own Dir
            use_metadata=True,
            axis_forward='-Z', # Forward
            axis_up='Y' # Up
        )
        obj.select_set(False)
        #print("Saved At: " + export_path + export_filename)

    # Reselect all objects
    for obj in selected_objects:
        obj.select_set(True)


# Operator to perform the export
class OBJECT_OT_mrwhimble_export_selected(bpy.types.Operator):
    bl_idname = "object.mrwhimble_export_selected_models"
    bl_label = "Export Selected Models"
    
    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="Path to export the FBX files",
        subtype='DIR_PATH'
    )
    
    def execute(self, context):
        original_transforms = mrwhimble_move_models_to_origin()
        #self.report({'INFO'}, "Exporting %d models to %r" % (len(bpy.context.selected_objects), self.export_path))
        absolute_export_path=bpy.path.abspath(self.export_path)
        mrwhimble_export_models_fbx(absolute_export_path)
        mrwhimble_move_models_to_original_positions(original_transforms)
        self.report({'INFO'}, "Exported %d models to %r" % (len(bpy.context.selected_objects), absolute_export_path))
        return {'FINISHED'}

class OBJECT_PT_mrwhimble_export_selected(bpy.types.Panel):
    bl_idname = "object_PT_mrwhimble_export_selected"
    bl_label = "Export Selected Models"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"
    
    def draw(self, context):
        if context.object == None:
            return
        
        layout = self.layout
        
        row = layout.row()
        row.prop(context.scene, "global_mrwhimble_export_selected_export_path")
        
        row = layout.row()
        props = row.operator("object.mrwhimble_export_selected_models")
        props.export_path = context.scene.global_mrwhimble_export_selected_export_path

# Register the operator and create a button in the UI
def register():
    
    bpy.types.Scene.global_mrwhimble_export_selected_export_path = bpy.props.StringProperty(
        name="Export Path",
        description="Path to export the FBX files",
        subtype='DIR_PATH'
    )
    
    bpy.utils.register_class(OBJECT_OT_mrwhimble_export_selected)
    bpy.utils.register_class(OBJECT_PT_mrwhimble_export_selected)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_mrwhimble_export_selected)
    bpy.utils.unregister_class(OBJECT_PT_mrwhimble_export_selected)
    del bpy.types.Object.global_mrwhimble_export_selected_export_path

# Entry point
if __name__ == "__main__":
    register()
