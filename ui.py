import bpy

class CutscenePanel(bpy.types.Panel):
    bl_label = "Cutscene Data"
    bl_idname = "OBJECT_PT_cutscene_data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Add UI elements for user data
        layout.prop(scene, "user_data1", text="User  Data 1")
        layout.prop(scene, "user_data2", text="User  Data 2")
        layout.prop(scene, "range_start", text="Range Start")
        layout.prop(scene, "range_end", text="Range End")
        layout.prop(scene, "alt_range_end", text="Alt Range End")
        layout.prop(scene, "section_duration", text="Section Duration")
        layout.prop(scene, "fade_out_duration", text="Fade Out Duration")
        layout.prop(scene, "fade_in_game_duration", text="Fade In Game Duration")
        layout.prop(scene, "fade_in_color", text="Fade In Color")
        layout.prop(scene, "blend_out_duration", text="Blend Out Duration")
        layout.prop(scene, "blend_out_offset", text="Blend Out Offset")
        layout.prop(scene, "fade_out_game_duration", text="Fade Out Game Duration")
        layout.prop(scene, "fade_in_cutscene_duration", text="Fade In Cutscene Duration")
        layout.prop(scene, "fade_out_color", text="Fade Out Color")
        layout.prop(scene, "day_cochours", text="Day CoC Hours")

        # Display custom properties of the selected object
        if context.active_object and "event_id" in context.active_object:
            layout.label(text=f"Event ID: {context.active_object['event_id']}")

def register():
    bpy.utils.register_class(CutscenePanel)

def unregister():
    bpy.utils.unregister_class(CutscenePanel)