"""Render frames to image sequence"""

from multiprocessing import Pool
from InstrumentPanel import InstrumentPanel

instrument_panel_image = InstrumentPanel()

def render_frames(frames:dict, output_folder:str, filename_prefix:str='image_'):
    """Render frame info to output image sequence

    Args:
        frames (dict): frame dict from calculate_frames
        output_folder (str): output folder for rendered images
    """
    p = Pool()
    num_zeros = len(str(len(frames['Frame'])))
    filepath_prefix = f'{output_folder}\\{filename_prefix}'
    for frame, altitude, course, speed, bank, pitch, valid in zip(frames['Frame'], frames['Altitude'], frames['Course'], frames['Speed'], frames['Bank'], frames['Pitch'], frames['Valid']):
        p.apply_async(render_frame, args=(altitude, course, speed, bank, pitch, frame, valid, filepath_prefix, num_zeros))
    p.close()
    p.join()

def render_frame(altitude, course, speed, bank, pitch, frame, valid, filepath_prefix, num_zeros):
    '''Render a single frame to an image file'''
    tmp_image = instrument_panel_image.build_image(altitude, course, speed, bank, pitch, valid)
    tmp_image.save(f'{filepath_prefix}{frame:0{num_zeros}d}.png', compress_level=1)
