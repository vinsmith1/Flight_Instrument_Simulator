# Script to create an image sequence of flight instruments using actual flight data logged by ForeFlight

import os
import time
import cProfile
from convert_tracklog import convert_tracklog
from calculate_frames import calculate_frames
from render_output import render_output
from write_dict_to_csv import write_dict_to_csv

def animate_instrument_panel(csv_filename):
    """Animate the instrument panel of an aircraft based on a tracklog file
    
    Args:
        csv_filename (string): full path to the tracklog file
    """
    time_benchmark_begin = time.time()
    module_name = 'build_instrument_panel'
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Started building instrument panel')

    animation_frame_rate = 30
    output_path = '.\\output'

    # Create output directory for rendered images if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {csv_filename}')
    time_convert_tracklog_begin = time.time()
    data = convert_tracklog(csv_filename)
    write_dict_to_csv(data, csv_filename.removesuffix('.csv') + '_output.csv')
    time_convert_tracklog_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {csv_filename} completed in {(time_convert_tracklog_end - time_convert_tracklog_begin):#.2f} seconds')

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Calculating frames')
    time_calculate_frames_begin = time.time()
    frames = calculate_frames(data, animation_frame_rate)
    write_dict_to_csv(frames, csv_filename.removesuffix('.csv') + '_frames.csv')
    time_calculate_frames_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Frames calculated in {(time_calculate_frames_end - time_calculate_frames_begin):#.2f} seconds')

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Rendering frames')
    time_render_output_begin = time.time()
    render_output(frames, output_path)
    time_render_output_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Rendered {len(frames['Frame'])} frames in {(time_render_output_end - time_render_output_begin):#.2f} seconds ({((len(frames['Frame']))/(time_render_output_end - time_render_output_begin)):#.2f} frames per second)')
    
    time_benchmark_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Finished building instrument panel')
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Script completed in {(time_benchmark_end - time_benchmark_begin):#.2f} seconds')

if __name__ == "__main__":
    # without profiling
    animate_instrument_panel("tracklog_test.csv")
    
    # with profiling
    # cProfile.run('animate_instrument_panel("tracklog_test.csv")', 'profile_results')
