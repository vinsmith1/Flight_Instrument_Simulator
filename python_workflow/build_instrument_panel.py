# Create video of heading indicator moving throughout
# needle position based on data extracted from ForeFlight track log
# 
# Several layers are merged together:
# - bottom: background of the heading indicator
# - card:   layer with cardinal directions and degrees that rotates according to heading
# - top:    45degree pointers and airplane outline
#
# ForeFlight track log format
# first three rows are headers
# fourth and remaining rows contain data
import os
import time
import csv
from convert_tracklog import convert_tracklog
import VideoWriter
import InstrumentPanel

def build_instrument_panel(csv_filename, logOnly=True):
    timeStart = time.time()
    outputList = []
    instrumentPanelImg = InstrumentPanel.InstrumentPanel()

    # Module name
    module_name = 'build_instrument_panel'
    output_path = '.\\output'
    if not os.path.exists(output_path): 
        # if the directory is not present then create it. 
        os.makedirs(output_path) 
    
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {csv_filename}')
    
    # load tracklog csv
    data = convert_tracklog(csv_filename, write_data_log=True)
       
    # set up video writers
    videoFrameRate = 30
    
    # Identify keyframes
    # Calculate keyframe number from timestamp
    # This was moved to the blender file so the keyframes could be calculated by blender according to the selected framerate
    keyframes = []
    for t in data['Timestamp']:
        keyframes.append(round(t * videoFrameRate))
    data['Keyframe'] = keyframes
        

    if not logOnly:
        videoInsPanel  = VideoWriter.VideoWriter(instrumentPanelImg.size(), videoFrameRate, outputPath = f'.\output\{csv_filename}_ALT_HI_GSI_output.mp4')

    # helper function
    def saveImage(heading, speed, altitude, bank, pitch, frame):
        tmpImg = instrumentPanelImg.buildImage(heading, speed, altitude, bank, pitch)
        tmpImg.save(f'.\\output\\InstrumentPanel_{frame:04d}.png')
        videoInsPanel.writeFrame(tmpImg)
    
    timestamp_start = data['Timestamp'][0]
    timestamp_last = timestamp_start
    altitude_last = data['Altitude'][0]
    heading_last = data['Course'][0]
    speed_last = data['Speed'][0]
    bank_last = data['Bank'][0]
    pitch_last = data['Pitch'][0]
    keyframe_start = data['Keyframe'][0]
    keyframe_last = keyframe_start

    i = 0
    for timestamp, altitude, heading, speed, bank, pitch, keyframe in zip(data['Timestamp'], data['Altitude'], data['Course'], data['Speed'], data['Bank'], data['Pitch'], data['Keyframe']):
        
        # calculate how much each value needs to change between tracklog entries
        #timestamp_change = timestamp - timestamp_last
        #if timestamp_change == 0:
        #    continue
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

        # figure out how many frames need to be created between this timestamp and the last timestamp (interframe)
        #interframes = timestamp_change * videoFrameRate
        interframes = keyframe_change
        
        
        # calculate heading and groundspeed change per interframe
        #timestamp_change_interframe = timestamp_change / interframes
        altitude_change_interframe = altitude_change / interframes
        heading_change_interframe = heading_change / interframes
        speed_change_interframe = speed_change / interframes
        bank_change_interframe = bank_change / interframes
        pitch_change_interframe = pitch_change / interframes

        # linearly interpolate the heading and ground speed changes for each interframe
        for frame in range(int(round(interframes))):
            i += 1
            #timestamp = timestamp_last + timestamp_change_interframe * frame
            altitude = altitude_last + altitude_change_interframe * frame
            rotation = heading_last + heading_change_interframe * frame
            speed = speed_last + speed_change_interframe * frame
            bank = bank_last + bank_change_interframe * frame
            pitch = pitch_last + pitch_change_interframe * frame
            outputList.append([timestamp, altitude, rotation, speed, bank, pitch,''])
            if not logOnly:
                saveImage(rotation, speed, altitude, bank, pitch, i)
        
        timestamp_last = timestamp
        altitude_last = altitude
        heading_last = heading
        speed_last = speed
        #print(f'tracklog row: {idx+1}, total frames processed: {i}, bank: {bank}, pitch: {pitch}')
        #if idx > 10:
        #    break

    #clipDuration = timestamp_last-timestamp_start

    if not logOnly:
        videoInsPanel.release()
        videoInsPanel = []

    #with open(outputCsvFilePath, 'w', newline='') as file:
    #    writer = csv.writer(file)
    #    writer.writerow(['Filename', outputCsvFilename])
    #    writer.writerow(['Start Time', timestamp_start])
    #    writer.writerow(['End Time', timestamp_last])
    #    writer.writerow(['Duration (sec)', clipDuration])
    #    writer.writerow(['Frames', i])
    #    writer.writerow(['Desired Framerate (fps)', videoFrameRate])
    #    writer.writerow(['Actual Framerate (fps)', float(i)/clipDuration])
    #    writer.writerow('')
    #    writer.writerow(['timestamp', 'Altitude', 'Course', 'Speed', ''])
    #    writer.writerows(outputList)

    timeEnd = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} {i+1} frames processed in {timeEnd-timeStart:#.1f} seconds / {(timeEnd-timeStart)/60:#.1f} minutes ({(i+1)/(timeEnd-timeStart):#.1f} images per second)')



if __name__ == "__main__":
    build_instrument_panel("tracklog_test", True)