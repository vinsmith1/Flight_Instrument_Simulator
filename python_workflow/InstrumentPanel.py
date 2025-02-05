from PIL import Image
from HeadingIndicator import HeadingIndicator
from GroundSpeedIndicator import GroundSpeedIndicator
from Altimeter import Altimeter
from AttitudeIndicator import AttitudeIndicator

class InstrumentPanel:
    """Class to build an instrument panel image by concatenating images from individual instrument classes

    Returns:
        _type_: _description_
    """
    # load source images
    def __init__(self):
        self.hi = HeadingIndicator()
        self.gsi = GroundSpeedIndicator()
        self.alt = Altimeter()
        self.ai = AttitudeIndicator()
        width = self.hi.width() + self.gsi.width() + self.alt.width() + self.ai.width()
        self.image = Image.new('RGBA', ( width, max(self.hi.height(), self.gsi.height(), self.alt.height(), self.ai.height()) ))

    def build_image(self, altitude=0, course=0, speed=0, bank=0, pitch=0):
        """Return an image of the instrument panel according to the input parameters

        Args:
            altitude (int, optional): _description_. Defaults to 0.
            course (int, optional): _description_. Defaults to 0.
            speed (int, optional): _description_. Defaults to 0.
            bank (int, optional): _description_. Defaults to 0.
            pitch (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        alt = self.alt.build_image(altitude)
        hi = self.hi.build_image(course)
        gsi = self.gsi.build_image(speed)
        ai = self.ai.build_image(bank, pitch)

        img = self.image.copy()
        col = 0
        img.paste(gsi, (col,0), gsi)
        col += gsi.width
        img.paste(hi, (col,0), hi)
        col += hi.width
        img.paste(alt, (col, 0), alt)
        col += alt.width
        img.paste(ai, (col, 0), ai)
        return img

    def size(self):
        """Return the size of the instrument panel image

        Returns:
            _type_: tuple describing the size of the image
        """
        return self.image.size
