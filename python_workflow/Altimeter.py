from PIL import Image

class Altimeter(object):
    '''Class for altimeter instrument'''
    
    def __init__(self, min_speed=25, min_speed_pointer_angle=0,
            max_speed=200, max_speed_pointer_angle=39,
            clockwise_positive=True):
        # y1: angle at low speed
        # y2: angle at high speed
        # x1: low speed
        # x2: high speed
        # CW_positive tells if the pointer should move clockwise with increasing speed
        self.x1 = min_speed
        self.y1 = min_speed_pointer_angle
        self.x2 = max_speed
        self.y2 = max_speed_pointer_angle
        self.CW_positive = clockwise_positive

        self.background = Image.open('.\input_images\ALT_background.png').convert('RGBA')
        self.hundredsPointer = Image.open('.\input_images\ALT_hundreds_indicator.png').convert('RGBA')
        self.thousandsPointer = Image.open('.\input_images\ALT_thousands_indicator.png').convert('RGBA')
        self.tenThousandsPointer = Image.open('.\input_images\ALT_ten_thousands_indicator.png').convert('RGBA')
    
    def buildImage(self, altitude):
        '''
        Returns an image of the altimter showing the indicated speed
        
            Parameters:
                speed (float): a value that indicates aircraft ground speed
            
            Returns
                imgTemp (Image): a PIL Image of the altimeter
        '''
        imgTemp = Image.new('RGBA', self.background.size, 'CYAN')
        imgTemp.paste(self.background, (0,0), self.background)
        
        imgTenThousandsPointerRotated = self.tenThousandsPointer.rotate(-altitude*0.0036)
        imgTemp.paste(imgTenThousandsPointerRotated, (0,0), imgTenThousandsPointerRotated)
        
        imgThousandsPointerRotated = self.thousandsPointer.rotate(-altitude*0.036)
        imgTemp.paste(imgThousandsPointerRotated, (0,0), imgThousandsPointerRotated)
        
        imgHundredsPointerRotated = self.hundredsPointer.rotate(-altitude*0.36)
        imgTemp.paste(imgHundredsPointerRotated, (0,0), imgHundredsPointerRotated)
                
        return imgTemp
    
    def size(self):
        return self.background.size

    def width(self):
        return int(self.background.width)
    
    def height(self):
        return int(self.background.height)