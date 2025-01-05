from tkinter import image_names
from PIL import Image

class AttitudeIndicator(object):
    """Class for AdditudeIndicator image"""
    def __init__(self):
        self.bottom = Image.open('.\input_images\AI_background.png').convert('RGBA')
        self.pitch = Image.open('.\input_images\AI_pitch.png').convert('RGBA')
        self.bank = Image.open('.\input_images\AI_bank.png').convert('RGBA')
        self.top = Image.open('.\input_images\AI_overlay.png').convert('RGBA')
    
    def buildImage(self, bank, pitch):
        imgPitch = Image.new('RGBA', self.bottom.size, 'CYAN')
        # slide pitch card up or down according to pitch value
        # scaling factor 2.35 (47/20) derived empirically
        imgPitch.paste(self.bottom, (0,0), self.bottom)
        imgPitch.paste(self.pitch, (0, int(pitch*2.35)), self.bottom)
        
        imgAI = Image.new('RGBA', self.top.size, 'CYAN')
        imgAI.paste(self.bottom, (0,0), self.bottom)
        
        imgPitchRotated= imgPitch.rotate(bank)        
        imgAI.paste(imgPitchRotated, (0,0), self.bottom)
        
        imgBankRotated = self.bank.rotate(bank)
        imgAI.paste(imgBankRotated, (0,0), imgBankRotated)
        
        imgAI.paste(self.top, (0,0), self.top)
        return imgAI
    
    def size(self):
        return self.top.size
    
    def width(self):
        return int(self.top.width)
    
    def height(self):
        return int(self.top.height)