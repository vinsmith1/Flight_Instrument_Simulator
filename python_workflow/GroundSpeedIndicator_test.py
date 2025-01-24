import os
import VideoWriter
import GroundSpeedIndicator

videoFrameRate = 30
output_path='.\\output\\GSI_test'

if not os.path.exists(output_path): 
        # if the directory is not present then create it. 
        os.makedirs(output_path) 

GSI = GroundSpeedIndicator.GroundSpeedIndicator()
GSI_video = VideoWriter.VideoWriter(GSI.size(), videoFrameRate, outputPath = output_path + '\\GSI_test.mp4')

# Create image/video sequence
for frame,speed in enumerate(range(0, 206, 1)):
    tmpGSI = GSI.build_image(speed)
    # Save image 
    tmpGSI.save(f'{output_path}\\GSI_{frame:04d}.png')
    # Write to video file
    GSI_video.writeFrame(tmpGSI)
    print(f'speed: {speed}, angle: {GSI.speed_to_angle(speed)}')

GSI_video.release()