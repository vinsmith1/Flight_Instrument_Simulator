import sys
from PIL import Image

class HeadingIndicator():
    """Class for HeadingIndicator image"""
    def __init__(self):
        '''Initialize the heading indicator image'''
        # Check if the background, compass card, and overlay images exist
        try:
            self.background = Image.open('.\\input_images\\HI_background.png').convert('RGBA')
            self.compasscard = Image.open('.\\input_images\\HI_compass_card.png').convert('RGBA')
            self.top = Image.open('.\\input_images\\HI_overlay.png').convert('RGBA')
        except FileNotFoundError as e:
            print(f'Can\'t open file: {e}')
            sys.exit(1)      

    def build_image(self, heading):
        '''Build a heading indicator image'''
        img = Image.new('RGBA', self.background.size)
        img.paste(self.background, (0,0), self.background)
        img_card_rotated = self.compasscard.rotate(heading)
        img.paste(img_card_rotated, (0,0), img_card_rotated)
        img.paste(self.top, (0,0), self.top)
        return img

    def size(self):
        """Return the size of the heading indicator image"""
        return self.background.size

    def width(self):
        """Return the width of the heading indicator image"""
        return int(self.background.width)

    def height(self):
        """Return the height of the heading indicator image"""
        return int(self.background.height)
