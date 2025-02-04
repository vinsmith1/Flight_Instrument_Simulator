import os
import HeadingIndicator

OUTPUT_PATH = '.\\output\\HI_test'

if not os.path.exists(OUTPUT_PATH):
        # if the directory is not present then create it.
        os.makedirs(OUTPUT_PATH) 

HI = HeadingIndicator.HeadingIndicator()

# Create image/video sequence
for frame, heading in enumerate(range(-20, 380, 1)):
    tmpALT = HI.build_image(heading)
    # Save image
    tmpALT.save(f'{OUTPUT_PATH}\\HI_{frame:04d}.png')
    print(f'Heading: {heading}')
