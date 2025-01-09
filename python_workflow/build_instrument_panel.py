import os
import time
import csv
from convert_tracklog import convert_tracklog
from calculate_frames import calculate_frames
from render_output import render_output

def build_instrument_panel(csv_filename, logOnly=True):
    #benchmark_time_start = time.time()
    #module_name = 'build_instrument_panel'
    #print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Started building instrument panel')
                   
    #output_path = '.\\output'
    #if not os.path.exists(output_path): 
    #    os.makedirs(output_path) 
    
    #print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {csv_filename}')
    
    # load tracklog csv
    data = convert_tracklog(csv_filename, write_data_log=True)
    
    animation_frame_rate = 30
    
    frames = calculate_frames(data, animation_frame_rate)


    write_outputframes_log = True
    if write_outputframes_log:
        # Write data dict to output csv file
        output_csv_filename = csv_filename.removesuffix('.csv') + '_output_frames.csv'    
        with open(output_csv_filename, 'w', newline='') as output_f:
            fieldnames = frames.keys()
            writer = csv.DictWriter(output_f, fieldnames = fieldnames)
            writer.writeheader()
            
            # For reference, data dict format is {key0:[key0data0,key0data1...],key1:[key1data0,key1data1...]}
            # to write the rows of the output csv file, need to grab the i'th value of each key for each row
            for i,row in enumerate(frames['Frame']):
                tempDict = {}
                for col in frames.keys():    
                    tempDict[col] = frames[col][i]
                writer.writerow(tempDict)
        
        

    #print(frames)

    # render_output(frames)


    #timeEnd = time.time()
    #print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} {i+1} frames processed in {timeEnd-benchmark_time_start:#.1f} seconds / {(timeEnd-benchmark_time_start)/60:#.1f} minutes ({(i+1)/(timeEnd-benchmark_time_start):#.1f} images per second)')



if __name__ == "__main__":
    # write only the csv output file?
    # True = only write the csv output file without overwriting the mp4 file
    # False = write video mp4 file and csv file
    logOnly = True
    build_instrument_panel("tracklog.csv", logOnly)