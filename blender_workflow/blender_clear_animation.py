# This is a copy of "clear_animation.py" within the InstrumentPanelAnimate.blend file. It is not intended to be run as a standalone script, but from within the Blender file.

# This script clears the animation data from all objects in the specified collections, and sets the z-rotation of each object to 0. It also sets the x and y location of the AI_static, AI_pitch, and AI_bank objects to the specified values.

import bpy

collections = ['GSI_static', 'GSI_pointer', 'AI_static', 'AI_bank', 'AI_pitch', 'ALT_static', 'ALT_ten_thousands_indicator', 'ALT_thousands_indicator', 'ALT_hundreds_indicator', 'HI_static', 'HI_compass_card']

for collection in collections:
    col = bpy.data.collections.get(collection)
    if col:
        for obj in col.objects:
            obj.animation_data_clear()
            obj.rotation_euler[2] = 0

AI_X = 0.0
AI_Y = 1.3
col = bpy.data.collections.get("AI_static")
if col:
    for obj in col.objects:
        obj.location[0] = AI_X
        obj.location[1] = AI_Y
col = bpy.data.collections.get("AI_pitch")
if col:
    for obj in col.objects:
        obj.location[0] = AI_X
        obj.location[1] = AI_Y
col = bpy.data.collections.get("AI_bank")
if col:
    for obj in col.objects:
        obj.location[0] = AI_X
        obj.location[1] = AI_Y
