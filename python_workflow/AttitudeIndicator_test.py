import os
import AttitudeIndicator

OUTPUT_PATH='.\\output\\AI_test'

if not os.path.exists(OUTPUT_PATH): 
    os.makedirs(OUTPUT_PATH)

AI = AttitudeIndicator.AttitudeIndicator()

# Create image/video sequence
counter = 0
for i,bank in enumerate(range(-45,46,5)):
    for j,pitch in enumerate(range(-20,21,5)):
        tmpAI = AI.build_image(bank, pitch)
        # Save image
        tmpAI.save(f'{OUTPUT_PATH}\\AI_{counter:04d}.png')
        print(f'Pitch: {pitch}, Bank: {bank}')
        counter += 1
