import os
import VideoWriter
import HeadingIndicator

videoFrameRate = 30
output_path = '.\\output\\HI_test'

if not os.path.exists(output_path): 
        # if the directory is not present then create it. 
        os.makedirs(output_path) 

HI = HeadingIndicator.HeadingIndicator()
HI_video = VideoWriter.VideoWriter(HI.size(), videoFrameRate, outputPath=output_path + '\\HI_test.mp4')

# Create image/video sequence
for frame, heading in enumerate(range(-20, 380, 1)):
    tmpALT = HI.build_image(heading)
    # Save image
    tmpALT.save(f'{output_path}\\HI_{frame:04d}.png')
    # Write image to video file
    HI_video.writeFrame(tmpALT)
    print(f'Heading: {heading}')
    
HI_video.release()