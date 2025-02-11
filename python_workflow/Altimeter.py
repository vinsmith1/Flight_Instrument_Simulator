import sys
from PIL import Image

class Altimeter():
    """Class for Altimeter instrument"""    
    def __init__(self):
        '''Initialize the altimeter image'''

        # Open background, hundreds, thousands, and ten thousands pointer images
        try:
            self.background = Image.open('.\\input_images\\ALT_background.png').convert('RGBA')
            self.hundreds_pointer = Image.open('.\\input_images\\ALT_hundreds_indicator.png').convert('RGBA')
            self.thousands_pointer = Image.open('.\\input_images\\ALT_thousands_indicator.png').convert('RGBA')
            self.ten_thousands_pointer = Image.open('.\\input_images\\ALT_ten_thousands_indicator.png').convert('RGBA')
        except FileNotFoundError as e:
            print(f'Can\'t open file: {e}')
            sys.exit(1)

    def build_image(self, altitude):
        '''
        Returns an image of the altimeter showing the indicated speed
        
            Parameters:
                speed (float): a value that indicates aircraft ground speed
            
            Returns
                imgTemp (Image): a PIL Image of the altimeter
        '''
        img = Image.new('RGBA', self.background.size)
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
