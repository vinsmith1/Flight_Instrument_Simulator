from PIL import Image

class GroundSpeedIndicator(object):
    """Class for ground speed indicator instrument

    Returns:
        _type_: _description_
    """
        
    def __init__(self, min_speed=25, min_speed_pointer_angle=0,
            max_speed=200, max_speed_pointer_angle=39):
        # y1: angle at low speed
        # y2: angle at high speed
        # x1: low speed
        # x2: high speed
        # CW_positive tells if the pointer should move clockwise with increasing speed
        self.x1 = min_speed
        self.y1 = min_speed_pointer_angle
        self.x2 = max_speed
        self.y2 = max_speed_pointer_angle

        self.background = Image.open('.\input_images\GSI_background.png').convert('RGBA')
        self.pointer = Image.open('.\input_images\GSI_pointer.png').convert('RGBA')
    
    def buildImage(self, speed):
        """Returns an image of the ground speed indicator showing the indicated speed

        Args:
            speed (float): a value between 0 and max_speed that represents ground speed

        Returns:
            Image: a PIL Image of the ground speed indicator indicating the desired speed
        """
        imgTemp = Image.new('RGBA', self.background.size, 'CYAN')
        imgTemp.paste(self.background, (0,0), self.background)
        imgPointerRotated = self.pointer.rotate(self.speed_to_angle(speed))
        imgTemp.paste(imgPointerRotated, (0,0), imgPointerRotated)
        return imgTemp
    
    def speed_to_angle(self, speed):
        '''Calculate pointer angle from the speed value'''
        # since the two are linearly related, use point-slope line equation to calculate angle
        #  y = (y2-y1)/(x2-x1)*(x-x1)+y1
        # values above the max speed or below the min speed are clamped at their given angles
        if speed <= self.x1:
            return self.y1
        elif speed >= self.x2:
            return self.y2
        else:
            y21 = (self.y2-self.y1)%-360
            x21 = (self.x2-self.x1)
            return y21/x21*(speed-self.x1)+self.y1

    def size(self):
        return self.background.size

    def width(self):
        return int(self.background.width)
    
    def height(self):
        return int(self.background.height)