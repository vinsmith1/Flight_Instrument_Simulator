import os
import time
import csv
import convert_tracklog
import calculate_frames
import render_output

def build_instrument_panel(csv_filename, logOnly=True):
    benchmark_time_start = time.time()
    module_name = 'build_instrument_panel'
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Started building instrument panel')
                   
    output_path = '.\\output'
    if not os.path.exists(output_path): 
        os.makedirs(output_path) 
    
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {csv_filename}')
    
    # load tracklog csv
    data = convert_tracklog(csv_filename, write_data_log=True)
    
    animation_frame_rate = 30
    
    frames = calculate_frames(data, animation_frame_rate)

    render_output(frames)


    timeEnd = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} {i+1} frames processed in {timeEnd-benchmark_time_start:#.1f} seconds / {(timeEnd-benchmark_time_start)/60:#.1f} minutes ({(i+1)/(timeEnd-benchmark_time_start):#.1f} images per second)')



if __name__ == "__main__":
    # write only the csv output file?
    # True = only write the csv output file without overwriting the mp4 file
    # False = write video mp4 file and csv file
    logOnly = True
    build_instrument_panel("tracklog.csv", logOnly)