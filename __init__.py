import bpy
from .cutimport import CutsceneImport
from .cutexport import CutsceneExport
from .ui import CutscenePanel

bl_info = {
    "name": "Cutsinator",
    "author": "The AA Teams",
    "description": "Grand Theft Auto V cutscene modding suite for Blender",
    "blender": (4, 0, 0),
    "version": (0, 0, 104),
    "category": "Import-Export",
}

def menu_func_import(self, context):
    self.layout.operator(CutsceneImport.bl_idname, text="Import Cutscene (.cut.pso.xml)")

def menu_func_export(self, context):
    self.layout.operator(CutsceneExport.bl_idname, text="Export Cutscene (.cut.pso.xml)")

def register():
    bpy.utils.register_class(CutsceneImport)
    bpy.utils.register_class(CutsceneExport)
    bpy.utils.register_class(CutscenePanel)

    # Add to the File menu
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


    bpy.types.Scene.user_data1 = bpy.props.StringProperty(name="User  Data 1")
    bpy.types.Scene.user_data2 = bpy.props.StringProperty(name="User  Data 2")
    bpy.types.Scene.range_start = bpy.props.IntProperty(name="Range Start")
    bpy.types.Scene.range_end = bpy.props.IntProperty(name="Range End")
    bpy.types.Scene.alt_range_end = bpy.props.IntProperty(name="Alt Range End")
    bpy.types.Scene.section_duration = bpy.props.FloatProperty(name="Section Duration")
    bpy.types.Scene.fade_out_duration = bpy.props.FloatProperty(name="Fade Out Duration")
    bpy.types.Scene.fade_in_game_duration = bpy.props.FloatProperty(name="Fade In Game Duration")
    bpy.types.Scene.fade_in_color = bpy.props.StringProperty(name="Fade In Color")
    bpy.types.Scene.blend_out_duration = bpy.props.FloatProperty(name="Blend Out Duration")
    bpy.types.Scene.blend_out_offset = bpy.props.FloatProperty(name="Blend Out Offset")
    bpy.types.Scene.fade_out_game_duration = bpy.props.FloatProperty(name="Fade Out Game Duration")
    bpy.types.Scene.fade_in_cutscene_duration = bpy.props.FloatProperty(name="Fade In Cutscene Duration")
    bpy.types.Scene.fade_out_color = bpy.props.StringProperty(name="Fade Out Color")
    bpy.types.Scene.day_cochours = bpy.props.IntProperty(name="Day CoC Hours")

def unregister():
    bpy.utils.unregister_class(CutsceneImport)
    bpy.utils.unregister_class(CutsceneExport)
    bpy.utils.unregister_class(CutscenePanel)

    # Remove from the File menu
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()