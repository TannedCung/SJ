import cv2
import numpy as np
from math import sqrt

class Detector():
    Cascade_path = "./data/haarcascade_frontalface_alt.xml"
    def __init__(self, detect_method='face'):
        self.face_cascade = cv2.CascadeClassifier(self.Cascade_path)
        self.green = (10,225,10)
        self.red = (10,10,225)
        self.cyan = (225,225,10)
        self.yellow = (10,225,225)
        self.color = self.cyan      # cyan for neutral mood

    def detect_v1(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
                                            gray,
                                            scaleFactor=1.2,
                                            minNeighbors=5,
                                            minSize=(32, 32)
                                            )
        return faces
    
    def mark_object(self, frame, locate):
        x,y,w,h = locate
        x_center = int(x+w/2)
        y_center = int(y+h/2)
        # draw a rectangle around the object
        cv2.rectangle(frame, (x,y), (x+w, y+h), self.color, thickness=1)
        cv2.line(frame, (x_center, y_center), (240,160), self.yellow, thickness=1)
        return int(sqrt((x_center-240)**2 + (y_center-160)**2))
