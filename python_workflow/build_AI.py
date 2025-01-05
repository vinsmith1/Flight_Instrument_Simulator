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

import time
import csv
import VideoWriter
import AttitudeIndicator

def build_AI(inputCsvFilnameWithoutExtension, logOnly=True):
    # other variables
    timeStart = time.time()
    outputList = []
    attitudeIndicatorImg = AttitudeIndicator.AttitudeIndicator()

    # load tracklog csv
    inputCsvFilename = inputCsvFilnameWithoutExtension + '.csv'
    print(f'[build_AI] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {inputCsvFilename}')
    outputCsvFilename = f'{inputCsvFilnameWithoutExtension}_AI_output.csv'
    outputCsvFilePath = f'.\output\{outputCsvFilename}'
    inputCsvFile = open(inputCsvFilename, newline='')
    log = csv.reader(inputCsvFile, delimiter=',')
    
    # determine number of records
    next(log)
    next(log)
    next(log)
    row_count = sum(1 for row in log)
    inputCsvFile.seek(0)
    log = csv.reader(inputCsvFile, delimiter=',')
    print(f'number of records: {row_count}')
    
    # skip the first three rows of the tracklog
    next(log)
    next(log)
    next(log)

    # set up video writers
    videoFrameRate = 30 # set to same as GoPro framerate

    if not logOnly:
        videoInsPanel  = VideoWriter.VideoWriter(attitudeIndicatorImg.size(), videoFrameRate, outputPath = f'D:\Videos\output\{inputCsvFilnameWithoutExtension}_AI_output.mp4')

    # helper function
    def saveImage(bank, pitch, frame=0):
        tmpImg = attitudeIndicatorImg.buildImage(bank, pitch)
        #tmpImg.save(f'D:\Videos\output\{inputFilnameWithoutExtension}_{frame:04d}.png')
        videoInsPanel.writeFrame(tmpImg)

    #process first record
    row = next(log)
    startTimestamp  = float(row[0])
    timestampLast   = float(row[0])
    bankLast        = float(row[6])
    pitchLast       = float(row[7])

    i = 0
    # process 2nd through last records
    for idx,row in enumerate(log):
        timestampCurrent    = float(row[0])
        # ignore blank values
        if len(row[6]) > 0:
            bankCurrent  =  float(row[6])
        if len(row[7]) > 0:
            pitchCurrent = float(row[7])
        
        # process only if there was a change or if this is the last record
        if ((bankCurrent == bankLast) or (pitchCurrent == pitchLast)) and not idx == (row_count - 2):
            # no change               or       no change              and        not last
            continue
        
        # calculate how much each value needs to change between tracklog entries
        timstampChange = timestampCurrent - timestampLast
        bankChange = bankCurrent - bankLast
        pitchChange = pitchCurrent - pitchLast

        # figure out how many frames need to be created between this timestamp and the last timestamp (interframe)
        interframes = timstampChange * videoFrameRate
        
        # calculate heading and groundspeed change per interframe
        timstampChangeInterframe = timstampChange / interframes
        bankChangeInterframe = bankChange / interframes
        pitchChangeInterframe = pitchChange / interframes
        
        # linearly interpolate the heading and ground speed changes for each interframe
        for frame in range(int(round(interframes))):
            i += 1
            timestamp = timestampLast  + timstampChangeInterframe*frame
            bank     = bankLast        + bankChangeInterframe*frame
            pitch    = pitchLast       + pitchChangeInterframe*frame
            outputList.append([timestamp, bank, pitch, ''])
            if not logOnly:
                saveImage(bank, pitch, i)
        
        timestampLast   = timestampCurrent
        bankLast        = bankCurrent
        pitchLast       = pitchCurrent
        #print(f'tracklog row: {idx+1}, total frames processed: {i}, bank: {bank}, pitch: {pitch}')
        #if idx > 10:
        #    break

    clipDuration = timestampLast-startTimestamp

    if not logOnly:
        videoInsPanel.release()
        videoInsPanel = []

    with open(outputCsvFilePath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', outputCsvFilename])
        writer.writerow(['Start Time', startTimestamp])
        writer.writerow(['End Time', timestampLast])
        writer.writerow(['Duration (sec)', clipDuration])
        writer.writerow(['Frames', i])
        writer.writerow(['Desired Framerate (fps)', videoFrameRate])
        writer.writerow(['Actual Framerate (fps)', float(i)/clipDuration])
        writer.writerow('')
        writer.writerow(['timestamp', 'Bank', 'Pitch', ''])
        writer.writerows(outputList)

    timeEnd = time.time()
    print(f'[build_AI] {time.strftime("%Y-%m-%d %H:%M:%S")} {i+1} frames processed in {timeEnd-timeStart:#.1f} seconds / {(timeEnd-timeStart)/60:#.1f} minutes ({(i+1)/(timeEnd-timeStart):#.1f} images per second)')

if __name__ == "__main__":
    build_AI("tracklog_test", True)