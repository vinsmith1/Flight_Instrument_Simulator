import sys
from PIL import Image

class AttitudeIndicator():
    """Class for AdditudeIndicator image"""
    def __init__(self):
        """Initialize the attitude indicator image"""
        try:
            self.background = Image.open('.\\input_images\\AI_background.png').convert('RGBA')
            self.pitch = Image.open('.\\input_images\\AI_pitch.png').convert('RGBA')
            self.bank = Image.open('.\\input_images\\AI_bank.png').convert('RGBA')
            self.overlay = Image.open('.\\input_images\\AI_overlay.png').convert('RGBA')
        except FileNotFoundError as e:
            print(f'Can\'t open file: {e}')
            sys.exit(1)

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
