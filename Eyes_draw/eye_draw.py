import cv2
import numpy as np
from time import sleep
import random
from math import tan, pi

class Draw():
    def __init__(self, thickness=1, radius=20, mood=(225,225,0)):
        self.thickness = thickness
        self.radius = radius
        self.edge_shift = int(self.thickness/2.0)
        self.mood = mood
        self.black = (0,0,0)

    def cal_4_corners(self, width, height, position, downHeight=0, angle=0):
        x, y = position
        height = height - downHeight        
        bl_pt = (int(x-width/2), int(y+height/2))
        br_pt = (int(x+width/2), int(y+height/2))
        if angle<0:
            angle = angle*pi/180
            tl_pt = (int(x-width/2), int(y-height/2))
            height = height - width*tan(abs(angle))
            tr_pt = (int(x+width/2), int(y-height/2))
        elif angle>0:
            angle = angle*pi/180
            tr_pt = (int(x+width/2), int(y-height/2))
            height = height - width*tan(abs(angle))
            tl_pt = (int(x-width/2), int(y-height/2))
        else:
            tl_pt = (int(x-width/2), int(y-height/2))
            tr_pt = (int(x+width/2), int(y-height/2))
        return tl_pt, tr_pt, bl_pt, br_pt




    def drawRoundRectangle(self, img, width, height, position, downHeight=0, angle=0):
        # print(position)
        tl_pt, tr_pt, bl_pt, br_pt = self.cal_4_corners(width, height, position, downHeight, angle)
        mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)
        #draw lines
        #top
        cv2.line(img, (tl_pt[0]+self.radius, tl_pt[1]), 
        (tr_pt[0]-self.radius, tr_pt[1]), self.mood, self.thickness)
        #bottom
        cv2.line(img, (bl_pt[0]+self.radius, bl_pt[1]), 
        (br_pt[0]-self.radius, br_pt[1]), self.mood, self.thickness)
        #left
        cv2.line(img, (tl_pt[0], tl_pt[1]+self.radius), 
        (bl_pt[0], bl_pt[1]-self.radius), self.mood, self.thickness)
        #right
        cv2.line(img, (tr_pt[0], tr_pt[1]+self.radius), 
        (br_pt[0], br_pt[1]-self.radius), self.mood, self.thickness)

        #corners
        # top lelf
        cv2.ellipse(img, (tl_pt[0]+self.radius, tl_pt[1]+self.radius), 
        (self.radius, self.radius), 90, 90, 180, self.mood, self.thickness)
        # top right
        cv2.ellipse(img, (tr_pt[0]-self.radius, tr_pt[1]+self.radius), 
        (self.radius, self.radius), -90, 0, 90, self.mood, self.thickness)
        # bot right
        cv2.ellipse(img, (br_pt[0]-self.radius, br_pt[1]-self.radius), 
        (self.radius, self.radius), 90, 270, 360, self.mood, self.thickness)
        # bot lelf
        cv2.ellipse(img, (bl_pt[0]+self.radius, bl_pt[1]-self.radius), 
        (self.radius, self.radius), -90, 180, 270, self.mood, self.thickness)       
        cv2.floodFill(img,mask=mask, seedPoint=position, newVal=self.mood)

    def erase(self, img, width, height, position, downHeight=0, angle=0):
        tl_pt, tr_pt, bl_pt, br_pt = self.cal_4_corners(width, height, position, downHeight, angle)
        mask = np.zeros((img.shape[0]+2, img.shape[1]+2), np.uint8)

        #draw lines
        #top
        cv2.line(img, (tl_pt[0]+self.radius, tl_pt[1]), 
        (tr_pt[0]-self.radius, tr_pt[1]), self.black, self.thickness)
        #bottom
        cv2.line(img, (bl_pt[0]+self.radius, bl_pt[1]), 
        (br_pt[0]-self.radius, br_pt[1]), self.black, self.thickness)
        #left
        cv2.line(img, (tl_pt[0], tl_pt[1]+self.radius), 
        (bl_pt[0], bl_pt[1]-self.radius), self.black, self.thickness)
        #right
        cv2.line(img, (tr_pt[0], tr_pt[1]+self.radius), 
        (br_pt[0], br_pt[1]-self.radius), self.black, self.thickness)

        #corners
        # top lelf
        cv2.ellipse(img, (tl_pt[0]+self.radius, tl_pt[1]+self.radius), 
        (self.radius, self.radius), 90, 90, 180, self.black, self.thickness)
        # top right
        cv2.ellipse(img, (tr_pt[0]-self.radius, tr_pt[1]+self.radius), 
        (self.radius, self.radius), -90, 0, 90, self.black, self.thickness)
        # bot right
        cv2.ellipse(img, (br_pt[0]-self.radius, br_pt[1]-self.radius), 
        (self.radius, self.radius), 90, 270, 360, self.black, self.thickness)
        # bot lelf
        cv2.ellipse(img, (bl_pt[0]+self.radius, bl_pt[1]-self.radius), 
        (self.radius, self.radius), -90, 180, 270, self.black, self.thickness)       
        cv2.floodFill(img,mask=mask, seedPoint=position, newVal=self.black)

    def erase_2(self, img):
        img = img*0


"""
drawer = Draw(mood=(255,255,25))
img = np.zeros((320, 480, 3), np.uint8)
a = 25
max = 150
alp = random.randrange(0,10)


back = False
while a<=150:
    drawer.drawRoundRectangle(img=img, width=int(120+a/5), height=a, position=(150,150), angle=alp)
    drawer.drawRoundRectangle(img=img, width=int(120+a/5), height=a, position=(350,150), angle=-alp)
    # print(img.shape)
    # sleep(2)
    cv2.imshow("test", img)

    # print(a)
    # drawer.erase(img=img, width=int(120+a/5), height=a, position=(150,150), angle=alp)
    # drawer.erase(img=img, width=int(120+a/5), height=a, position=(350,150), angle=-alp)
    # drawer.erase_2(img=img)
    img = img*0
    # cv2.imshow("test1", img)
    # 
    # drawer.erase_2(img=img)

    if not back:
        a = a+18
    else:
        a = a-18
    if a>=max-18:
        back = True
        sleep(4)
        alp = random.randrange(-30,30)
        print(alp)
    if a<=50:
        back = False
        alp = random.randrange(-30,30)
        print(alp)
    if cv2.waitKey(5) == 27:
        break
"""
