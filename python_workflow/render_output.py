from multiprocessing import Pool
import InstrumentPanel
instrument_panel_image = InstrumentPanel.InstrumentPanel()

def render_output(frames:dict, output_folder:str):
    """Render frame info to output image sequence

    Args:
        frames (dict): frame dict from calculate_frames
        output_folder (str): output folder for rendered images
    """
    p = Pool()
    for frame, altitude, course, speed, bank, pitch in zip(frames['Frame'], frames['Altitude'], frames['Course'], frames['Speed'], frames['Bank'], frames['Pitch']):
        p.apply_async(render_frame, args=(altitude, course, speed, bank, pitch, frame, path))
    p.close()
    p.join()

def render_frame(altitude, course, speed, bank, pitch, frame, path):
    tmp_image = instrument_panel_image.build_image(altitude, course, speed, bank, pitch)
    tmp_image.save(f'{output_folder}\\InstrumentPanel_{frame:04d}.png', compress_level=1)
