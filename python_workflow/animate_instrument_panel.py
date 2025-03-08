# Script to create an image sequence of flight instruments using actual flight data logged by ForeFlight

import os
import time
import cProfile
from convert_tracklog import convert_tracklog
from calculate_frames import calculate_frames
from render_frames import render_frames
from render_video import render_video
from write_dict_to_csv import write_dict_to_csv

def animate_instrument_panel(tracklog_filepath:str, frame_rate:int, output_folder:str, logging=False):
    """Animate the instrument panel of an aircraft based on a tracklog file
    
    Args:
        tracklog_filename (string): full path to the tracklog file
    """
    time_benchmark_begin = time.time()
    module_name = 'build_instrument_panel'
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Started building instrument panel')

    # Create output directory for rendered images if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Extract just the filename from the full path
    tracklog_filename = os.path.basename(tracklog_filepath)

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {tracklog_filepath}')
    time_convert_tracklog_begin = time.time()
    data = convert_tracklog(tracklog_filepath)
    if logging:
        write_dict_to_csv(data, len(data["Timestamp"]), f'{output_folder}\\{tracklog_filename.removesuffix('.csv')}_output.csv')
    time_convert_tracklog_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {tracklog_filepath} completed in {(time_convert_tracklog_end - time_convert_tracklog_begin):#.2f} seconds')

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Calculating data for all frames')
    time_calculate_frames_begin = time.time()
    frames = calculate_frames(data, frame_rate)
    if logging:
        write_dict_to_csv(frames, len(frames["Frame"]), f'{output_folder}\\{tracklog_filename.removesuffix('.csv')}_frames.csv')
    time_calculate_frames_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} {len(frames["Frame"])} frames calculated in {(time_calculate_frames_end - time_calculate_frames_begin):#.2f} seconds')

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Rendering frames')
    time_render_frames_begin = time.time()
    render_frames(frames, output_folder)
    time_render_frames_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Rendered {len(frames['Frame'])} frames in {(time_render_frames_end - time_render_frames_begin):#.2f} seconds ({((len(frames['Frame']))/(time_render_frames_end - time_render_frames_begin)):#.2f} frames per second)')

    render_video_flag = False
    if render_video_flag:
        print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Rendering video')
        time_render_video_begin = time.time()
        render_video(output_folder, frame_rate)
        time_render_video_end = time.time()
        print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Rendered video in {(time_render_video_end - time_render_video_begin):#.2f} seconds')

    time_benchmark_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Finished building instrument panel')
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Script completed in {(time_benchmark_end - time_benchmark_begin):#.2f} seconds')

if __name__ == "__main__":
    framerate = 30
    output_folder = r'F:\Flying Videos\2022-07-09\instrument_panel'
    # tracklog_file = 'tracklog-58B30DBB-8A5E-415B-BF35-B41CE9DD29DC.csv'
    # tracklog_file = 'tracklog_test.csv'
    # tracklog_file = 'tracklog-2819609B-5140-4011-B8EC-52F2FBB4D875.csv'
    tracklog_filepath = r'F:\Flying Videos\2022-07-09\tracklog-2022-07-09.csv'

    # without profiling
    animate_instrument_panel(tracklog_filepath, framerate, output_folder, logging=True)

    # with profiling
    # cProfile.run('animate_instrument_panel(tracklog, framerate, output_folder)', 'profile_results')
