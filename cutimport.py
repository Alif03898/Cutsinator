import bpy
from bpy_extras.io_utils import ImportHelper
from .xml_handler import XMLHandler

class CutsceneImport(bpy.types.Operator, ImportHelper):
    bl_idname = "import.cutscene"
    bl_label = "Import Cutscene"
    filename_ext = ".cut.pso.xml"
    filter_glob: bpy.props.StringProperty(default="*.cut.pso.xml", options={'HIDDEN'})

    def execute(self, context):
        if self.filepath.endswith('.cut.pso.xml'):
            return self.import_cutscene(context, self.filepath)
        return {'CANCELLED'}

    def import_cutscene(self, context, filepath):
        xml_handler = XMLHandler(filepath)
        cutscene_data = xml_handler.read_cutscene()

        # Check if there is an active object
        if context.object is None:
            self.report({'WARNING'}, "No active object found. Please select an object to import cutscene data.")
            return {'CANCELLED'}

        # Clear existing markers and regions (optional)
        context.scene.timeline_markers.clear()
        for seq in context.scene.sequence_editor.sequences_all:
            context.scene.sequence_editor.sequences.remove(seq)

        # Get the frame rate of the scene
        fps = context.scene.render.fps

        # Process events
        max_frame = 0  # To track the maximum frame number

        for event in cutscene_data['events']:
            object_id = event['iObjectId']
            fTime = event['fTime']  # This is in seconds

            # Convert seconds to frames
            frame_number = int(fTime * fps)

            # Get event type, default to "Unknown" if not found
            event_type = next((arg['cName'] for arg in cutscene_data['event_args'] if arg['iObjectId'] == object_id), None)

            # Check if event_type is None or empty
            if event_type is None:
                event_type = "Unknown"

            # Create a marker for object events (load/unload)
            if "load" in event_type.lower() or "unload" in event_type.lower():
                marker = context.scene.timeline_markers.new(name=f"Marker_{object_id}", frame=frame_number)
                marker['object_id'] = object_id  # Store object_id in marker properties
                marker['event_type'] = event_type  # Store event type in marker properties

            # Create a region for cutscene events
            else:
                # Create a region (cutscene event)
                region = context.scene.sequence_editor.sequences.new_scene(
                    name=f"Region_{object_id}",
                    scene=context.scene,
                    frame_start=frame_number,
                    channel=1  # Specify the channel for the region
                )
                region.frame_final_duration = 50  # Set the duration of the region to 50 frames

                # Store additional data in the region
                region['object_id'] = object_id  # Store object_id in region properties
                region['event_type'] = event_type  # Store event type in region properties

                # If the event ID is 21, create a plane for subtitles
                if object_id == 21:
                    self.create_subtitle_plane(context, frame_number)

            # Update max_frame to find the highest frame number
            max_frame = max(max_frame, frame_number)

        # Set the end frame of the scene to the maximum frame detected
        context.scene.frame_end = max_frame

        return {'FINISHED'}

    def create_subtitle_plane(self, context, frame_number):
        # Create a new plane
        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        plane = context.active_object
        plane.name = "Subtitle_Plane"

        # Create a new material
        mat = bpy.data.materials.new(name="Subtitle_Material")
        mat.diffuse_color = (1.0, 1.0, 0.0, 1.0)  # Yellow color
        plane.data.materials.append(mat)

        # Set custom property for event ID
        plane["event_id"] = 21  # Set the event ID

        # Position the plane above the camera or in a suitable location
        plane.location.z = 1  # Adjust the height as needed

        # Optionally, you can set the plane to be a child of the camera or another object
        # camera = context.scene.camera
        # if camera:
        #     plane.parent = camera
