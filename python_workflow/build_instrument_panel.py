# Create video of heading indicator moving throughout
# needle position based on data extracted from ForeFlight track log
# 
# Several layers are merged together:
# - bottom: background of the heading indicator
# - card:   layer with cardinal directions and degrees that rotates according to heading
# - top:    45degree pointers and airplane outline

import os
import time
import csv
from convert_tracklog import convert_tracklog
import VideoWriter
import InstrumentPanel

def build_instrument_panel(csv_filename, logOnly=True):
    benchmark_time_start = time.time()
    module_name = 'build_instrument_panel'
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Started building instrument panel')
    
    outputList = []
    instrumentPanelImg = InstrumentPanel.InstrumentPanel()
   
    output_path = '.\\output'
    if not os.path.exists(output_path): 
        os.makedirs(output_path) 
    
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {csv_filename}')
    
    # load tracklog csv
    data = convert_tracklog(csv_filename, write_data_log=True)
    
    animation_frame_rate = 30
    
    # Identify keyframes
    # Calculate keyframe number from timestamp
    # This was moved to the blender file so the keyframes could be calculated by blender according to the selected framerate
    keyframes = []
    for t in data['Timestamp']:
        keyframes.append(round(t * animation_frame_rate))
    data['Keyframe'] = keyframes
        

    if not logOnly:
        videoInsPanel  = VideoWriter.VideoWriter(instrumentPanelImg.size(), animation_frame_rate, outputPath = f'.\output\{csv_filename}_ALT_HI_GSI_output.mp4')

    # helper function
    def saveImage(heading, speed, altitude, bank, pitch, frame):
        tmpImg = instrumentPanelImg.buildImage(heading, speed, altitude, bank, pitch)
        tmpImg.save(f'.\\output\\InstrumentPanel_{frame:04d}.png')
        # videoInsPanel.writeFrame(tmpImg)
    
    # timestamp_start = data['Timestamp'][0]
    # timestamp_last = timestamp_start
    altitude_last = data['Altitude'][0]
    heading_last = data['Course'][0]
    speed_last = data['Speed'][0]
    bank_last = data['Bank'][0]
    pitch_last = data['Pitch'][0]
    keyframe_start = data['Keyframe'][0]
    keyframe_last = keyframe_start

    i = 0
    for altitude, heading, speed, bank, pitch, keyframe, valid in zip(data['Altitude'], data['Course'], data['Speed'], data['Bank'], data['Pitch'], data['Keyframe'], data['Valid']):
        keyframe_change = keyframe - keyframe_last
        if keyframe_change == 0:
            continue
        altitude_change = altitude - altitude_last
        # how much the heading needs to change between tracklog entries
        # "rotational interpolation" from https://stackoverflow.com/questions/2708476/rotation-interpolation
        heading_change = (((heading - heading_last) + 180) % 360) - 180
        speed_change = speed - speed_last
        bank_change = bank - bank_last
        pitch_change = pitch - pitch_last     
        
        # calculate between keyframes
        altitude_change_interframe = altitude_change / keyframe_change
        heading_change_interframe = heading_change / keyframe_change
        speed_change_interframe = speed_change / keyframe_change
        bank_change_interframe = bank_change / keyframe_change
        pitch_change_interframe = pitch_change / keyframe_change

        # linearly interpolate the heading and ground speed changes for each interframe
        for frame in range(int(round(keyframe_change))):
            i += 1
            altitude = altitude_last + altitude_change_interframe * frame
            rotation = heading_last + heading_change_interframe * frame
            speed = speed_last + speed_change_interframe * frame
            bank = bank_last + bank_change_interframe * frame
            pitch = pitch_last + pitch_change_interframe * frame
            outputList.append([i, valid, altitude, rotation, speed, bank, pitch])
            if not logOnly:
                saveImage(rotation, speed, altitude, bank, pitch, i)
        
        keyframe_last = keyframe
        altitude_last = altitude
        heading_last = heading
        speed_last = speed
        bank_last = bank
        pitch_last = pitch


    if not logOnly:
        videoInsPanel.release()
        videoInsPanel = []

    output_csv_filename = csv_filename.removesuffix('.csv') + '_output_frames.csv'
    with open(output_csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Frame', 'Altitude', 'Course', 'Speed', 'Bank', 'Pitch'])
        writer.writerows(outputList)

    timeEnd = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} {i+1} frames processed in {timeEnd-benchmark_time_start:#.1f} seconds / {(timeEnd-benchmark_time_start)/60:#.1f} minutes ({(i+1)/(timeEnd-benchmark_time_start):#.1f} images per second)')



if __name__ == "__main__":
    build_instrument_panel("tracklog_test", True)