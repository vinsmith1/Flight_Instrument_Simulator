import os
from PIL import Image

class HeadingIndicator():
    """Class for HeadingIndicator image"""
    def __init__(self):
        # Check if the background, compass card, and overlay images exist
        if not os.path.exists('.\input_images\HI_background.png'):
            raise FileNotFoundError('Background image not found')
        if not os.path.exists('.\input_images\HI_compass_card.png'):
            raise FileNotFoundError('Compass card image not found')
        if not os.path.exists('.\input_images\HI_overlay.png'):
            raise FileNotFoundError('Overlay image not found')

        self.background = Image.open('.\input_images\HI_background.png').convert('RGBA')
        self.compasscard = Image.open('.\input_images\HI_compass_card.png').convert('RGBA')
        self.top = Image.open('.\input_images\HI_overlay.png').convert('RGBA')

    def build_image(self, heading):
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
