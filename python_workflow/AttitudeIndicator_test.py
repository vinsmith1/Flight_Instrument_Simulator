import os
import VideoWriter
import AttitudeIndicator

videoFrameRate = 30
output_path='.\\output\\AI_test'

if not os.path.exists(output_path): 
        # if the directory is not present then create it. 
        os.makedirs(output_path) 

AI = AttitudeIndicator.AttitudeIndicator()
AI_video = VideoWriter.VideoWriter(AI.size(), videoFrameRate, outputPath=output_path + '\\AI_test.mp4')

# Create image/video sequence
for i,bank in enumerate(range(-90,91,5)):
    for j,pitch in enumerate(range(-20,21,1)):
        tmpAI = AI.build_image(bank, pitch)
        # Save image
        tmpAI.save(f'{output_path}\\AI_{i*j:04d}.png')
        # Write image to video file
        AI_video.writeFrame(tmpAI)
        print(f'Pitch: {pitch}, Bank: {bank}')

AI_video.release()