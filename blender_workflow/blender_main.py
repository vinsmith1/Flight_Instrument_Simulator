# This is a copy of "main.py" within the InstrumentPanelAnimate.blend. It is not intended to be run as a standalone script.
import sys
import bpy
import os
import math
import csv
import time

blend_filename = bpy.path.basename(bpy.context.blend_data.filepath)
tracklog = 'tracklog.csv'
framerate = 30

# ********* HELPER FUNCTIONS *************

def speed_to_angle(speed):
    """Calculate GSI pointer angle from the speed value

    Args:
        speed (float): speed value

    Returns:
        float: pointer angle for animation of ground speed indicator
    """
    # since the two are linearly related, use point-slope line equation to calculate angle
    #  y = (y2-y1)/(x2-x1)*(x-x1)+y1
    # values above the max speed or below the min speed are clamped at their given angles
    x1 = 25  # min_speed
    y1 = 0   # min_speed_pointer_angle
    x2 = 200 # max_speed
    y2 = 39  # max_speed_pointer_angle
    if speed <= x1:
        return y1
    elif speed >= x2:
        return y2
    else:
        y21 = (y2-y1)%-360
        x21 = (x2-x1)
        return y21/x21*(speed-x1)+y1

def convert_tracklog(input_csv_filename=None):
    """Convert a ForeFlight tracklog in csv format to an output format for use in animating graphical flight instruments in Blender

    Args:
        inputCsvFilename (_type_, optional): _description_. Defaults to None.
    """
    # Validate input argument....just check that the file is a .csv
    if not input_csv_filename or not str(input_csv_filename).endswith('.csv'):
        print('[convertTrackLog] Error: invalid file')
        return None
  
    f = open(input_csv_filename, newline='')
    # log = csv.reader(data, delimiter=',') # <-- this was the old method of doing it
    # Read the entire file at once instead of line-by-line
    raw_input_data = list(csv.reader(f, delimiter=','))
    
    # Omit the first two rows from the ForeFlight log as these contain other information
    header = raw_input_data[2]
    raw_row_data = raw_input_data[3:]
    
    # Remove the trailing rows of raw_row_data where any item in the row is an empty string
    # Do this by appending raw_row_data by row to a new list, stopping once a row with an empty string is reached
    # Speed and course values will typically be empty strings before the other values. This is probably caused by turning off the Sentry while ForeFlight is still recording the tracklog.
    filtered_row_data = []
    for row in raw_row_data:
        if '' not in row:
            filtered_row_data.append(row)
        else:
            break

    # Convert all items in filtered_row_data to float
    float_list = []
    for row in filtered_row_data:
        float_list.append(list(float(item) for item in row))
    
    # Convert to dictionary so columns can be processed by name
    data = dict()
    for colidx,col in enumerate(header):
        data[col] = [row[colidx] for row in float_list]

    # Headers
    # 00 = Timestamp
    # 01 = Latitude
    # 02 = Longitude
    # 03 = Altitude
    # 04 = Course
    # 05 = Speed
    # 06 = Bank
    # 07 = Pitch
    # 08 = Horizontal Error
    # 09 = Vertical Error
    
    # Eliminate unneeded columns
    data.pop('Latitude')
    data.pop('Longitude')
    data.pop('Horizontal Error')
    data.pop('Vertical Error')
    
    # Convert Timestamp to elapsed time
    start_time = data['Timestamp'][0]
    elapsed_times = []
    for item in data['Timestamp']:
        elapsed_times.append(item-start_time)
    data['Timestamp'] = elapsed_times
    
    # Calculate keyframe number from timestamp
    # This was moved to the blender file so the keyframes could be calculated by blender according to the selected framerate
    #keyframes = []
    #for t in data['Timestamp']:
    #    keyframes.append(round(t * framerate))
    #data['Keyframe'] = keyframes
    
    # Create a column identifying if a row contains "Valid" data
    # If course = -1.0 and speed = 0.0, "valid" should be 0, otherwise valid should be 1
    # Looking at a few logs shows that course = -1 and speed = 0 always at the same time, so it is sufficient to just check one
    valid = []
    for c in data['Course']:
        if c < 0:
            valid.append(False)
        else:
            valid.append(True)
    data['Valid'] = valid

    # Modify course to eliminate wrapping from 359° <-> 0°
    # The input is data['Course'], which is overwritten with the adjusted course
    # For each iteration of the list:
    #  Adjusted course (output) is 0 until the first valid course is reached (-1 = non-valid)
    #  After the first valid course is reached, any future instances of -1 do not change the adjusted course
    adjusted_course = []
    initialized = False
    current_course = 0

    for course, valid in zip(data['Course'], data['Valid']):
        if not valid:
            # Before initialization, replace -1 with 0; after, repeat the last valid angle
            adjusted_course.append(current_course)
            continue

        if not initialized:
            # Initialize with the first non-`-1` angle
            initialized = True
            current_course = course
            adjusted_course.append(current_course)
            continue

        # Calculate the difference considering wrap around
        delta = course - (current_course % 360)
        if delta > 180:
            delta -= 360
        elif delta < -180:
            delta += 360

        current_course += delta
        adjusted_course.append(current_course)

    data['Course'] = adjusted_course
    
    write_data_log = True
    if write_data_log:
        # Write data dict to output csv file
        output_csv_filename = input_csv_filename.removesuffix('.csv') + '_blenderoutput.csv'
            
        with open(output_csv_filename, 'w', newline='') as output_f:
            fieldnames = data.keys()
            writer = csv.DictWriter(output_f, fieldnames = fieldnames)
            writer.writeheader()
            
            # For reference, data dict format is {key0:[key0data0,key0data1...],key1:[key1data0,key1data1...]}
            # to write the rows of the output csv file, need to grab the i'th value of each key for each row
            for i,row in enumerate(data['Timestamp']):
                tempDict = {}
                for col in data.keys():    
                    tempDict[col] = data[col][i]
                writer.writerow(tempDict)

    return data




# ************* MAIN FUNCTION ***************
benchmark_time_start = time.time()
# load data file
current_path = bpy.path.abspath('//')
print(current_path)
csv_file = current_path + tracklog
print(f'[{blend_filename}] {time.strftime("%Y-%m-%d %H:%M:%S")} Start processing {csv_file}')
data = convert_tracklog(csv_file)

# Calculate the keyframes using the timestamp and the scene's framerate
bpy.context.scene.render.fps = framerate
# Calculate keyframe number from timestamp
# This was moved to the blender file so the keyframes could be calculated by blender according to the selected framerate
keyframes = []
for t in data['Timestamp']:
    keyframes.append(round(t * framerate))
data['Keyframe'] = keyframes

# convert the 'Keyframe' and 'Valid' data back to int
#col_to_int = ('Keyframe', 'Valid')
#for col in col_to_int:
#    temp = []
#    for val in data[col]:
#        temp.append(int(val))
#    data[col] = temp
# set number of keyframes
bpy.context.scene.frame_start = data['Keyframe'][0]
bpy.context.scene.frame_end = data['Keyframe'][-1]


# === headers ===
# Timestamp
# Altitude
# Course
# Speed
# Bank
# Pitch
# Valid

# Set location of GSI
GSI_X = -2.6
GSI_Y = 1.3
col = bpy.data.collections.get("GSI_static")
if col:
    for obj in col.objects:
        obj.location[0] = GSI_X
        obj.location[1] = GSI_Y
col = bpy.data.collections.get("GSI_pointer")
if col:
    for obj in col.objects:
        obj.location[0] = GSI_X
        obj.location[1] = GSI_Y

# Animate rotation of GSI pointer
print(f'[{blend_filename}] {time.strftime("%Y-%m-%d %H:%M:%S")} Set keyframes for GSI')
col = bpy.data.collections.get("GSI_pointer")
if col:
    # Clear animation data
    for obj in col.objects:
        obj.animation_data_clear()
    # Add anmiation data at the appropriate keyframes
    for key_frame, speed in zip(data['Keyframe'], data['Speed']):
        for obj in col.objects:
            obj.select_set(True)
            obj.rotation_euler[2] = math.radians(speed_to_angle(speed))
            obj.keyframe_insert('rotation_euler', frame = key_frame)
            obj.select_set(False)


# Set location of AI
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
        
# Animate AI
# Pitch and bank data only seems to change very 8-12 seconds in the captured data.
# If a keyframe is added for every data point the AI moves only when the data changes, which happens basically every 8-12 seconds.
# The animation algorithm for the AI should only add a keyframe if the pitch or bank has changed
pitch_last = data['Pitch'][0]
bank_last = data['Bank'][0]
print(f'[{blend_filename}] {time.strftime("%Y-%m-%d %H:%M:%S")} Set keyframes for AI')
# Bank
col = bpy.data.collections.get("AI_bank")
if col:
    # Clear animation data
    for obj in col.objects:
        obj.animation_data_clear()
    # Add anmiation data at the appropriate keyframes
    for key_frame, bank, pitch in zip(data['Keyframe'], data['Bank'], data['Pitch']):
        bank_rad = math.radians(-bank)
        if (bank == bank_last) and (pitch == pitch_last):
            continue
        for obj in col.objects:
            obj.select_set(True)
            obj.rotation_euler[2] = bank_rad
            obj.keyframe_insert('rotation_euler', frame = key_frame)
            obj.select_set(False)
        bank_last = bank
        pitch_last = pitch
# Pitch
# Pitch scale: location vector should be -0.405 when pitch is +20 degrees --> -0.405 / 20 = 0.02025
pitch_scale_factor = -0.02025
pitch_last = data['Pitch'][0]
bank_last = data['Bank'][0]
col = bpy.data.collections.get("AI_pitch")
if col:
    # Clear animation data
    for obj in col.objects:
        obj.animation_data_clear()
    # Add anmiation data at the appropriate keyframes
    for key_frame, bank, pitch in zip(data['Keyframe'], data['Bank'], data['Pitch']):
        bank_rad = math.radians(-bank)
        if (bank == bank_last) and (pitch == pitch_last):
            continue
        # Pitch is the vector and may need to be scaled
        pitch_scaled = pitch * pitch_scale_factor
        # Need to do a bit of vector transformation since the pitch card movement is relative to the bank angle
        # X and Y location depends on pitch and bank
        # X is Pitch * sin(bank)
        pitch_x = pitch_scaled * math.sin(bank_rad) + AI_X
        # Y is Pitch * cos(bank)
        pitch_y = pitch_scaled * math.cos(bank_rad) + AI_Y
        for obj in col.objects:
            obj.select_set(True)
            # Rotation is the same as bank
            obj.rotation_euler[2] = bank_rad
            obj.location[0] = pitch_x
            obj.location[1] = pitch_y
            obj.keyframe_insert('location', frame = key_frame)
            obj.keyframe_insert('rotation_euler', frame = key_frame)
            obj.select_set(False)
        bank_last = bank
        pitch_last = pitch

# Set location of ALT
ALT_X = 2.6
ALT_Y = 1.3
col = bpy.data.collections.get("ALT_static")
if col:
    for obj in col.objects:
        obj.location[0] = ALT_X
        obj.location[1] = ALT_Y
col = bpy.data.collections.get("ALT_hundreds_indicator")
if col:
    for obj in col.objects:
        obj.location[0] = ALT_X
        obj.location[1] = ALT_Y
col = bpy.data.collections.get("ALT_thousands_indicator")
if col:
    for obj in col.objects:
        obj.location[0] = ALT_X
        obj.location[1] = ALT_Y
col = bpy.data.collections.get("ALT_ten_thousands_indicator")
if col:
    for obj in col.objects:
        obj.location[0] = ALT_X
        obj.location[1] = ALT_Y

# Animate ALT pointers
print(f'[{blend_filename}] {time.strftime("%Y-%m-%d %H:%M:%S")} Set keyframes for ALT')
col = bpy.data.collections.get("ALT_hundreds_indicator")
if col:
    # Clear animation data
    for obj in col.objects:
        obj.animation_data_clear()
    # Add anmiation data at the appropriate keyframes
    for key_frame, altitude in zip(data['Keyframe'], data['Altitude']):
        for obj in col.objects:
            obj.select_set(True)
            obj.rotation_euler[2] = math.radians(altitude * -0.36)
            obj.keyframe_insert('rotation_euler', frame = key_frame)
            obj.select_set(False)
col = bpy.data.collections.get("ALT_thousands_indicator")
if col:
    # Clear animation data
    for obj in col.objects:
        obj.animation_data_clear()
    # Add anmiation data at the appropriate keyframes
    for key_frame, altitude in zip(data['Keyframe'], data['Altitude']):
        for obj in col.objects:
            obj.select_set(True)
            obj.rotation_euler[2] = math.radians(altitude * - 0.036)
            obj.keyframe_insert('rotation_euler', frame = key_frame)
            obj.select_set(False)
col = bpy.data.collections.get("ALT_ten_thousands_indicator")
if col:
    # Clear animation data
    for obj in col.objects:
        obj.animation_data_clear()
    # Add anmiation data at the appropriate keyframes
    for key_frame, altitude in zip(data['Keyframe'], data['Altitude']):
        for obj in col.objects:
            obj.select_set(True)
            obj.rotation_euler[2] = math.radians(altitude * -0.0036)
            obj.keyframe_insert('rotation_euler', frame = key_frame)
            obj.select_set(False)


# Set location of HI
HI_X = 0.0
HI_Y = -1.3
col = bpy.data.collections.get("HI_static")
if col:
    for obj in col.objects:
        obj.location[0] = HI_X
        obj.location[1] = HI_Y
col = bpy.data.collections.get("HI_compass_card")
        
# Animate HI
print(f'[{blend_filename}] {time.strftime("%Y-%m-%d %H:%M:%S")} Set keyframes for HI')
col = bpy.data.collections.get("HI_compass_card")
if col:
    # Clear animation data
    for obj in col.objects:
        obj.animation_data_clear()
    # Add anmiation data at the appropriate keyframes
    for key_frame,course in zip(data['Keyframe'], data['Course']):
        for obj in col.objects:
            obj.select_set(True)
            obj.rotation_euler[2] = math.radians(course)
            obj.keyframe_insert('rotation_euler', frame = key_frame)
            obj.select_set(False)

print(f'[{blend_filename}] {time.strftime("%Y-%m-%d %H:%M:%S")} Finished in {time.time()-benchmark_time_start:#.1f} seconds')