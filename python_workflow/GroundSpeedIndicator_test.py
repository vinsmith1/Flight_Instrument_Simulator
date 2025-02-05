import os
import GroundSpeedIndicator

OUTPUT_PATH='.\\output\\GSI_test'

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

GSI = GroundSpeedIndicator.GroundSpeedIndicator()

# Create image sequence
for frame,speed in enumerate(range(0, 206, 1)):
    tmpGSI = GSI.build_image(speed)
    # Save image
    tmpGSI.save(f'{OUTPUT_PATH}\\GSI_{frame:04d}.png')
    print(f'speed: {speed}, angle: {GSI.speed_to_angle(speed)}')
