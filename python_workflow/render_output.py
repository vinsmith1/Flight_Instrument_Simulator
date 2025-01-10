import InstrumentPanel

def render_output(frames, path):
    # render frame info to output images or video file
    instrumentPanelImg = InstrumentPanel.InstrumentPanel()
    for frame, altitude, course, speed, bank, pitch in zip(frames['Frame'], frames['Altitude'], frames['Course'], frames['Speed'], frames['Bank'], frames['Pitch']):
        tmpImg = instrumentPanelImg.buildImage(altitude, course, speed, bank, pitch)
        tmpImg.save(f'{path}\\InstrumentPanel_{frame:04d}.png')