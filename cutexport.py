import bpy
from bpy_extras.io_utils import ExportHelper
from .xml_handler import XMLHandler

class CutsceneExport(bpy.types.Operator, ExportHelper):
    bl_idname = "export.cutscene"
    bl_label = "Export Cutscene"
    filename_ext = ".cut.pso.xml"  # Change the extension here
    filter_glob: bpy.props.StringProperty(default="*.cut.pso.xml", options={'HIDDEN'})

    def execute(self, context):
        return self.export_cutscene(context, self.filepath)

    def export_cutscene(self, context, filepath):
        xml_handler = XMLHandler(filepath)

        cutscene_data = {
            'events': [],
            'event_args': [],
            'cutscene_objects': [],
            'load_events': [],
            'attributes': [],
            'additional_attributes': {}
        }

        # Iterate through objects in the scene
        for obj in bpy.context.scene.objects:
            # Check for custom property 'event_id'
            if "event_id" in obj:
                event_id = obj["event_id"]
                # Assuming you want to export the plane's position and other relevant data
                position = obj.location
                # Add the subtitle event to the cutscene data
                cutscene_data['events'].append({
                    'iObjectId': event_id,
                    'fTime': position.z / context.scene.render.fps  # Example: using Z position as time in seconds
                })

        # Write the cutscene data to XML
        xml_handler.write_cutscene(cutscene_data)

        self.report({'INFO'}, "Cutscene exported successfully.")
        return {'FINISHED'}