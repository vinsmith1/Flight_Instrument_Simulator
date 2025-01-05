import numpy as np
import cv2

class VideoWriter():
    '''Class for VideoWriter object that writes video file from frames'''
    def __init__(self, frameSize=(300,300), frameRate=30, outputPath='output.mp4'):
        #fourcc = cv2.VideoWriter_fourcc(*'avc1') # processed at 28.6 frames per sec, much smaller than mp4v
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # processed at 27.6 frames per sec
        #fourcc = cv2.VideoWriter_fourcc(*'X264')
        self.video = cv2.VideoWriter(outputPath, fourcc, frameRate, frameSize)
    
    def release(self):
        self.video.release()
    
    def writeFrame(self, image):
        self.video.write(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))