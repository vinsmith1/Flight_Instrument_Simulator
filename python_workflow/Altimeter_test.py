import os
import Altimeter

OUTPUT_PATH = '.\\output\\ALT_test'

if not os.path.exists(OUTPUT_PATH):
    # if the directory is not present then create it.
    os.makedirs(OUTPUT_PATH)

ALT = Altimeter.Altimeter()

# Create image/video sequence
for frame, altitude in enumerate(range(0, 10000, 9)):
    tmpALT = ALT.build_image(altitude)
    # Save image
    tmpALT.save(f'{OUTPUT_PATH}\\ALT_{frame:04d}.png')
    print(f'Altitude: {altitude}')
