import os
import VideoWriter
import Altimeter

videoFrameRate = 60
output_path = '.\\output\\ALT_test'

if not os.path.exists(output_path): 
        # if the directory is not present then create it. 
        os.makedirs(output_path) 

ALT = Altimeter.Altimeter()
ALT_video = VideoWriter.VideoWriter(ALT.size(), videoFrameRate, outputPath=output_path + '\\ALT_test.mp4')

# Create image/video sequence
for frame, altitude in enumerate(range(0, 10000, 10)):
    tmpALT = ALT.build_image(altitude)
    # Save image
    tmpALT.save(f'{output_path}\\ALT_{frame:04d}.png')
    # Write image to video file
    ALT_video.writeFrame(tmpALT)
    print(f'Altitude: {altitude}')
    
ALT_video.release()