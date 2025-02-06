from multiprocessing import Pool
import InstrumentPanel
instrument_panel_image = InstrumentPanel.InstrumentPanel()

def render_output(frames, path):
    """Render frame info to output image sequence

    Args:
        frames (_type_): _description_
        path (_type_): _description_
    """
    p = Pool()
    for frame, altitude, course, speed, bank, pitch in zip(frames['Frame'], frames['Altitude'], frames['Course'], frames['Speed'], frames['Bank'], frames['Pitch']):
        p.apply_async(render_frame, args=(altitude, course, speed, bank, pitch, frame, path))
    p.close()
    p.join()

def render_frame(altitude, course, speed, bank, pitch, frame, path):
    tmp_image = instrument_panel_image.build_image(altitude, course, speed, bank, pitch)
    tmp_image.save(f'{path}\\InstrumentPanel_{frame:04d}.png', compress_level=1)

if __name__ == '__main__':
    render_output()
