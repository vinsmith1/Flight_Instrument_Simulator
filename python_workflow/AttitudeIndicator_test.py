import os
import AttitudeIndicator

OUTPUT_PATH='.\\output\\AI_test'

if not os.path.exists(OUTPUT_PATH):
        # if the directory is not present then create it.
        os.makedirs(OUTPUT_PATH)

AI = AttitudeIndicator.AttitudeIndicator()

# Create image/video sequence
for i,bank in enumerate(range(-90,91,5)):
    for j,pitch in enumerate(range(-20,21,1)):
        tmpAI = AI.build_image(bank, pitch)
        # Save image
        tmpAI.save(f'{OUTPUT_PATH}\\AI_{i*j:04d}.png')

        print(f'Pitch: {pitch}, Bank: {bank}')
