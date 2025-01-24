import os
from PIL import Image

class AttitudeIndicator(object):
    """Class for AdditudeIndicator image"""
    def __init__(self):
        # Check if the background, pitch, bank, and overlay images exist
        if not os.path.exists('.\input_images\AI_background.png'):
            raise FileNotFoundError('Background image not found')
        if not os.path.exists('.\input_images\AI_pitch.png'):
            raise FileNotFoundError('Pitch image not found')
        if not os.path.exists('.\input_images\AI_bank.png'):
            raise FileNotFoundError('Bank image not found')
        if not os.path.exists('.\input_images\AI_overlay.png'):
            raise FileNotFoundError('Overlay image not found')

        self.bottom = Image.open('.\input_images\AI_background.png').convert('RGBA')
        self.pitch = Image.open('.\input_images\AI_pitch.png').convert('RGBA')
        self.bank = Image.open('.\input_images\AI_bank.png').convert('RGBA')
        self.top = Image.open('.\input_images\AI_overlay.png').convert('RGBA')

    def build_image(self, bank, pitch):
        """Build an attitude indicator image

        Args:
            bank (_type_): aircraft bank angle in degrees
            pitch (_type_): aircraft pitch angle in degrees

        Returns:
            _type_: _description_
        """
        img_pitch = Image.new('RGBA', self.bottom.size, 'CYAN')
        # slide pitch card up or down according to pitch value
        # scaling factor 2.35 (47/20) derived empirically
        img_pitch.paste(self.bottom, (0,0), self.bottom)
        img_pitch.paste(self.pitch, (0, int(pitch*2.35)), self.bottom)

        img_ai = Image.new('RGBA', self.top.size, 'CYAN')
        img_ai.paste(self.bottom, (0,0), self.bottom)

        img_pitch_rotated= img_pitch.rotate(bank)        
        img_ai.paste(img_pitch_rotated, (0,0), self.bottom)

        img_bank_rotated = self.bank.rotate(bank)
        img_ai.paste(img_bank_rotated, (0,0), img_bank_rotated)

        img_ai.paste(self.top, (0,0), self.top)
        return img_ai

    def size(self):
        """Return the size of the attitude indicator image"""
        return self.top.size

    def width(self):
        """Return the width of the attitude indicator image"""
        return int(self.top.width)

    def height(self):
        """Return the height of the attitude indicator image"""
        return int(self.top.height)
