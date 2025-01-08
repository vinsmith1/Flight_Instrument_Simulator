import VideoWriter
import InstrumentPanel

def render_output(frames):
    # render frame info to output images or video file

    instrumentPanelImg = InstrumentPanel.InstrumentPanel()

#if not logOnly:
    #    videoInsPanel  = VideoWriter.VideoWriter(instrumentPanelImg.size(), animation_frame_rate, outputPath = f'.\output\{csv_filename}_ALT_HI_GSI_output.mp4')

    # helper function
    def saveImage(heading, speed, altitude, bank, pitch, frame):
        tmpImg = instrumentPanelImg.buildImage(heading, speed, altitude, bank, pitch)
        tmpImg.save(f'.\\output\\InstrumentPanel_{frame:04d}.png')
        videoInsPanel.writeFrame(tmpImg)

    if not logOnly:
        videoInsPanel.release()
        videoInsPanel = []

    output_csv_filename = csv_filename.removesuffix('.csv') + '_output_frames.csv'
    with open(output_csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Frame', 'Altitude', 'Course', 'Speed', 'Bank', 'Pitch'])
        writer.writerows(outputList)