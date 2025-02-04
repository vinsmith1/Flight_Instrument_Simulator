import os
from PIL import Image

class AttitudeIndicator():
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

        self.background = Image.open('.\input_images\AI_background.png').convert('RGBA')
        self.pitch = Image.open('.\input_images\AI_pitch.png').convert('RGBA')
        self.bank = Image.open('.\input_images\AI_bank.png').convert('RGBA')
        self.overlay = Image.open('.\input_images\AI_overlay.png').convert('RGBA')
        # slide pitch card up or down according to pitch value
        # scaling factor derived empirically
        self.pitch_scaling_factor = 120/20
        self.pitch_height_offset = (self.pitch.height - self.background.height)/2

    def build_image(self, bank, pitch):
        """Build an attitude indicator image

        Args:
            bank (_type_): aircraft bank angle in degrees
            pitch (_type_): aircraft pitch angle in degrees

        Returns:
            _type_: _description_
        """
        img_ai = Image.new('RGBA', self.background.size)
        img_ai.paste(self.background, (0,0))

        img_pitch = Image.new('RGBA', self.background.size)
        img_pitch.paste(self.background, (0,0))
        pitch_offset = int(pitch * self.pitch_scaling_factor - self.pitch_height_offset)
        img_pitch.paste(self.pitch, (0, pitch_offset))
        img_pitch_rotated = img_pitch.rotate(bank)
        img_ai.paste(img_pitch_rotated, (0,0), self.background)

        img_bank_rotated = self.bank.rotate(bank)
        img_ai.paste(img_bank_rotated, (0,0), img_bank_rotated)

        img_ai.paste(self.overlay, (0,0), self.overlay)
        return img_ai

    def size(self):
        """Return the size of the attitude indicator image"""
        return self.overlay.size

    def width(self):
        """Return the width of the attitude indicator image"""
        return int(self.overlay.width)

    def height(self):
        """Return the height of the attitude indicator image"""
        return int(self.overlay.height)
