from PIL import Image

class HeadingIndicator(object):
    """Class for HeadingIndicator image"""
    def __init__(self):
        self.background = Image.open('.\input_images\HI_background.png').convert('RGBA')
        self.compasscard = Image.open('.\input_images\HI_compass_card.png').convert('RGBA')
        self.top = Image.open('.\input_images\HI_overlay.png').convert('RGBA')
    
    def buildImage(self, heading):
        imgTemp = Image.new('RGBA', self.background.size, 'CYAN')
        imgTemp.paste(self.background, (0,0), self.background)
        imgCardRotated = self.compasscard.rotate(heading)
        imgTemp.paste(imgCardRotated, (0,0), imgCardRotated)
        imgTemp.paste(self.top, (0,0), self.top)
        return imgTemp
    
    def size(self):
        return self.background.size

    def width(self):
        return int(self.background.width)
    
    def height(self):
        return int(self.background.height)