import os
import time
from convert_tracklog import convert_tracklog
from calculate_frames import calculate_frames
from render_output import render_output
from write_dict_to_csv import write_dict_to_csv

def animate_instrument_panel(csv_filename):
    """Animate the instrument panel of an aircraft based on a tracklog file
    
    Args:
        csv_filename (string): full path to the tracklog file
    """
    benchmark_time_start = time.time()
    module_name = 'build_instrument_panel'
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Started building instrument panel')

    animation_frame_rate = 30
    output_path = '.\\output'

    # Create output directory for rendered images if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Processing {csv_filename}')
    data = convert_tracklog(csv_filename)
    write_dict_to_csv(data, csv_filename.removesuffix('.csv') + '_output.csv')

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Calculating frames')
    frames = calculate_frames(data, animation_frame_rate)
    write_dict_to_csv(frames, csv_filename.removesuffix('.csv') + '_frames.csv')

    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Rendering frames')
    render_output(frames, output_path)

    time_end = time.time()
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} {len(frames['Frame'])} frames processed in {time_end-benchmark_time_start:#.1f} seconds / {(time_end-benchmark_time_start)/60:#.1f} minutes ({(len(frames['Frame'])+1)/(time_end-benchmark_time_start):#.1f} images per second)')
    print(f'[{module_name}] {time.strftime("%Y-%m-%d %H:%M:%S")} Finished building instrument panel')

if __name__ == "__main__":
    animate_instrument_panel("tracklog_test.csv")
