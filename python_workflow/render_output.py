import InstrumentPanel

def render_output(frames, path):
    """Render frame info to output image sequence

    Args:
        frames (_type_): _description_
        path (_type_): _description_
    """
    instrument_panel_image = InstrumentPanel.InstrumentPanel()
    for frame, altitude, course, speed, bank, pitch in zip(frames['Frame'], frames['Altitude'], frames['Course'], frames['Speed'], frames['Bank'], frames['Pitch']):
        tmp_image = instrument_panel_image.build_image(altitude, course, speed, bank, pitch)
        tmp_image.save(f'{path}\\InstrumentPanel_{frame:04d}.png')
