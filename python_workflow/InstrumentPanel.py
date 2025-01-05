# Create video of heading indicator moving throughout
# needle position based on data extracted from ForeFlight track log
# 
# Several layers are merged together:
# - bottom: background of the heading indicator
# - card:   layer with cardinal directions and degrees that rotates according to heading
# - top:    45degree pointers and airplane outline
#
# ForeFlight track log format
# first three rows are headers
# fourth and remaining rows contain data
from PIL import Image
from HeadingIndicator import HeadingIndicator
from GroundSpeedIndicator import GroundSpeedIndicator
from Altimeter import Altimeter
from AttitudeIndicator import AttitudeIndicator

class InstrumentPanel:

    # load source images

    def __init__(self):
        self.HI = HeadingIndicator()
        self.GSI = GroundSpeedIndicator()
        self.ALT = Altimeter()
        self.AI = AttitudeIndicator()
        width = self.HI.width() + self.GSI.width() + self.ALT.width() + self.AI.width()
        self.imgTemp = Image.new('RGBA', ( width, max(self.HI.height(), self.GSI.height(), self.ALT.height(), self.AI.height()) ), 'CYAN')

    def buildImage(self, heading=0, speed=0, altitude=0, bank=0, pitch=0):
        tmpGSI = self.GSI.buildImage(speed)
        tmpHI = self.HI.buildImage(heading)
        tmpALT = self.ALT.buildImage(altitude)
        tmpAI = self.AI.buildImage(bank, pitch)
               
        imgTemp = self.imgTemp.copy()
        col = 0
        imgTemp.paste(tmpGSI, (col,0), tmpGSI)
        col += tmpGSI.width
        imgTemp.paste(tmpHI, (col,0), tmpHI)
        col += tmpHI.width
        imgTemp.paste(tmpALT, (col, 0), tmpALT)
        col += tmpALT.width
        imgTemp.paste(tmpAI, (col, 0), tmpAI)
        return imgTemp
    
    def size(self):
        return self.imgTemp.size