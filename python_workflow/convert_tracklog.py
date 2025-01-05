# Filename: convert_tracklog.py
# Date: December 1, 2024
# Author: Vincent Smith
# 
# Description:
# Converts a ForeFlight track log in csv format into a new csv with only the data needed to generate the graphics for the instrument panel simulator in blender
#
# The script extracts the Timestamp, Altitude, Course, Speed, Bank, and Pitch data from the ForeFlight csv file to the output csv file.
# A "Valid" column is generated to indicate when course = -1 (course and speed are -1 essentially when the plane is stopped on the ground)
# Course data is modified so that they don't wrap around from 359 to 0 and from 0 to 359 as the course changes.
# Speed data is modified so that -1 is changed to 0

import time
import csv


def convert_tracklog(input_csv_filename=None, write_data_log=False):
    """Convert a ForeFlight tracklog in csv format to an output format for use in animating graphical flight instruments in Blender

    Args:
        inputCsvFilename (str, optional): Filename of csv file to be processed. Defaults to None.
        write_data_log (bool, optional): Write output log file?. Defaults to False.
    
    Returns:
        dict: Data necessary for further processing
    """
    module_name = 'convert_tracklog'
    # Track time for benchmarking purpose
    benchmark_time_start = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Start processing {input_csv_filename}')

    # Validate input argument....just check that the file is a .csv
    if not input_csv_filename or not str(input_csv_filename).endswith('.csv'):
        print('[{module_name}] Error: invalid file')
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
            valid.append(0)
        else:
            valid.append(1)
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

    if write_data_log:
        # Write data dict to output csv file
        output_csv_filename = input_csv_filename.removesuffix('.csv') + '_output.csv'
            
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
        
        print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Output file {output_csv_filename} contains {len(data["Timestamp"])} records') 
    
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Finished in {time.time()-benchmark_time_start:#.1f} seconds')    
    
    return data

if __name__ == "__main__":
    convert_tracklog('tracklog.csv', True)