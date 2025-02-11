from multiprocessing import Pool
import InstrumentPanel
instrument_panel_image = InstrumentPanel.InstrumentPanel()

class InstrumentPanelRenderer():
    def __init__(self, frames: dict, output_folder: str, filename_prefix: str = 'image_'):
        self.frames = frames
        self.output_folder = output_folder
        self.filepath_prefix = f'.\\{output_folder}\\{filename_prefix}'
        self.p = Pool()
        self.num_zeros = len(str(len(self.frames['Frame'])))

    def render_output(self):
        for frame, altitude, course, speed, bank, pitch in zip(self.frames['Frame'], self.frames['Altitude'], self.frames['Course'], self.frames['Speed'], self.frames['Bank'], self.frames['Pitch']):
            self.p.apply_async(self.render_frame, args=(altitude, course, speed, bank, pitch, frame))
        self.p.close()
        self.p.join()

    def render_frame(self, altitude, course, speed, bank, pitch, frame):
        tmp_image = instrument_panel_image.build_image(altitude, course, speed, bank, pitch)
        tmp_image.save(f'{self.filepath_prefix}{frame:0{self.num_zeros}d}.png', compress_level=1)



#def render_output(frames:dict, output_folder:str, filename_prefix:str='image_'):
#    """Render frame info to output image sequence
#
#    Args:
#        frames (dict): frame dict from calculate_frames
#        output_folder (str): output folder for rendered images
#    """
#    p = Pool()
#    num_zeros = len(len(frames['Frame']))
#    
#    for frame, altitude, course, speed, bank, pitch in zip(frames['Frame'], frames['Altitude'], frames['Course'], frames['Speed'], frames['Bank'], frames['Pitch']):
#        p.apply_async(render_frame, args=(altitude, course, speed, bank, pitch, frame, output_folder))
#    p.close()
#    p.join()
#
# def render_frame(altitude, course, speed, bank, pitch, frame, output_folder, filename_prefix):
#    tmp_image = instrument_panel_image.build_image(altitude, course, speed, bank, pitch)
#    tmp_image.save(f'{output_folder}\\{filename_prefix}{frame:04d}.png', compress_level=1)
