import os
from PIL import Image

class Altimeter(object):
    """Class for Altimeter instrument"""    
    def __init__(self, min_speed=25, min_speed_pointer_angle=0, max_speed=200, max_speed_pointer_angle=39, clockwise_positive=True):
        # y1: angle at low speed
        # y2: angle at high speed
        # x1: low speed
        # x2: high speed
        # CW_positive tells if the pointer should move clockwise with increasing speed
        self.x1 = min_speed
        self.y1 = min_speed_pointer_angle
        self.x2 = max_speed
        self.y2 = max_speed_pointer_angle
        self.cw_positive = clockwise_positive # currently not used

        # Check if background, hundreds, thousands, and ten thousands pointer images exist
        if not os.path.exists('.\input_images\ALT_background.png'):
            raise FileNotFoundError('Background image not found')
        if not os.path.exists('.\input_images\ALT_hundreds_indicator.png'):
            raise FileNotFoundError('Hundreds indicator image not found')
        if not os.path.exists('.\input_images\ALT_thousands_indicator.png'):
            raise FileNotFoundError('Thousands indicator image not found')
        if not os.path.exists('.\input_images\ALT_ten_thousands_indicator.png'):
            raise FileNotFoundError('Ten thousands indicator image not found')

        self.background = Image.open('.\input_images\ALT_background.png').convert('RGBA')
        self.hundreds_pointer = Image.open('.\input_images\ALT_hundreds_indicator.png').convert('RGBA')
        self.thousands_pointer = Image.open('.\input_images\ALT_thousands_indicator.png').convert('RGBA')
        self.ten_thousands_pointer = Image.open('.\input_images\ALT_ten_thousands_indicator.png').convert('RGBA')

    def build_image(self, altitude):
        '''
        Returns an image of the altimter showing the indicated speed
        
            Parameters:
                speed (float): a value that indicates aircraft ground speed
            
            Returns
                imgTemp (Image): a PIL Image of the altimeter
        '''
        img = Image.new('RGBA', self.background.size, 'CYAN')
        img.paste(self.background, (0,0), self.background)

        img_ten_thousands_pointer_rotated = self.ten_thousands_pointer.rotate(-altitude*0.0036)
        img.paste(img_ten_thousands_pointer_rotated, (0,0), img_ten_thousands_pointer_rotated)

        img_thousands_pointer_rotated = self.thousands_pointer.rotate(-altitude*0.036)
        img.paste(img_thousands_pointer_rotated, (0,0), img_thousands_pointer_rotated)

        img_hundreds_pointer_rotated = self.hundreds_pointer.rotate(-altitude*0.36)
        img.paste(img_hundreds_pointer_rotated, (0,0), img_hundreds_pointer_rotated)

        return img

    def size(self):
        """Return the size of the altimeter image"""
        return self.background.size

    def width(self):
        """Return the width of the altimeter image"""
        return int(self.background.width)

    def height(self):
        """Return the height of the altimeter image"""
        return int(self.background.height)
