from Eyes_draw.eye_draw import *
import cv2
import numpy as np
from time import sleep, time
import threading


class Move():
    def __init__(self):
        self.left_eye = (135,160)
        self.right_eye = (345,160)
        self.left_eye_size = (150, 150)
        self.right_eye_size = (150, 150)
        self.min_height = 50
        self.happy_neg_height = 90
        self.angry_neg_height = 35
        self.img = np.zeros((320,480,3), np.uint8)
        self.angle = 0
        self.pre_time = 0
        self.cur_time = time()
        # cv2.imshow("test", self.img)
        self.blink_step = 5
        self.offset_step = 50
        # mood
        self.happy = (10,225,10)
        self.neutral = (225,225,10)
        self.angry = (50,50,225)
        self.sad = (204,0,255)
        self.sad_angle = [5,15]
        self.angry_angle = [-30,-20]
        # paramaters
        self.artist = Draw(mood=self.neutral)
        self.max_offsetX = 50
        self.max_offsetY = 100
        self.move_flag = False
        self.blink_flag = False
        self.lock = threading.Lock()

    def cal_widthNheight(self, offsetX, offsetY):
        # if offset>0 the eyes go to the right and vice versal
        if abs(offsetX) > self.max_offsetX:
            offsetX = int(self.max_offsetX*(offsetX/abs(offsetX)))
            print ("max X")
        if abs(offsetY) > self.max_offsetY:
            offsetY = int(self.max_offsetY*(offsetY/abs(offsetY)))
            print ("max Y")
     
        self.left_eye = (135+offsetX, 160+offsetY)
        self.right_eye = (345+offsetX, 160+offsetY)
        # recal the size
        self.left_eye_size = (int(150-offsetX*0.1*150/self.max_offsetX), int(150-(offsetX*0.2*150/self.max_offsetX)-(abs(offsetY)*0.15*150/self.max_offsetY)))
        self.right_eye_size = (int(150+offsetX*0.1*150/self.max_offsetX), int(150+(offsetX*0.2*150/self.max_offsetX)-(abs(offsetY)*0.15*150/self.max_offsetY)))
        
    def blink(self, interval_time=4):
        left_step = int((self.left_eye_size[1]-self.min_height)/5)
        right_step = int((self.right_eye_size[1]-self.min_height)/5)
        # print("jump in blink")
        # self.blink_step = True
        openup = False
        done = False
        while not done: # and self.move_flag == False:  # blink_step = 1,2,3,4,5
            # self.lock.acquire()
            if openup:
                self.left_eye_size = (self.left_eye_size[0], self.left_eye_size[1]+left_step)
                self.right_eye_size = (self.right_eye_size[0], self.right_eye_size[1]+right_step)
                self.blink_step +=1
            else:
                self.left_eye_size = (self.left_eye_size[0], self.left_eye_size[1]-left_step)
                self.right_eye_size = (self.right_eye_size[0], self.right_eye_size[1]-right_step)
                self.blink_step -=1
            # sleep(1)
            self.update()
            if self.blink_step>=5:
                openup = False
                self.pre_time = time()
                done = True
                # sleep(1)
            elif self.blink_step <=1:
                openup = True
                # sleep(1)
            if cv2.waitKey(5) == 27:
                break
            # self.lock.release()
    
    def eyestrain(self):
        self.cur_time = time()
        if self.cur_time - self.pre_time > 4:
            return 1
        else:
            return 0

    def eye_move_interpole(self, x, y, interval=10):
        cur_pos = ((self.left_eye[0]+self.right_eye[0])/2, (self.left_eye[1]+self.right_eye[1])/2)
        # print("cur_pos:{}".format(cur_pos))
        x_dis = x-(self.left_eye[0]+self.right_eye[0])/2
        y_dis = y-(self.left_eye[1]+self.right_eye[1])/2
        steps = int(max(abs(x_dis), abs(y_dis))//interval)
        # print ("go to x:{}   y:{}".format(x,y))
        # print ("actually go to x:{}  y:{}".format())
        if steps > 1:
            x_odd_gap = x_dis//steps 
            x_last_gap = x_dis%steps
            y_odd_gap = y_dis//steps
            y_last_gap = y_dis%steps
            for i in range(steps):
                offsetX = int(cur_pos[0]+x_odd_gap*(i+1)-240)
                offsetY = int(cur_pos[1]+y_odd_gap*(i+1)-160)
                self.cal_widthNheight(offsetX,offsetY)
                self.update()
                cv2.waitKey(1)
            # offsetX = int((cur_pos[0]+x_odd_gap*steps+x_last_gap-240)/2)
            # offsetY = int((cur_pos[1]+y_odd_gap*steps+y_last_gap-160)/2)   
            # self.cal_widthNheight(offsetX, offsetY)
            # self.update()
            print("---------")
        else: 
            offsetX = int(x-240)
            offsetY = int(y-160)
            self.cal_widthNheight(offsetX, offsetY)
            self.update()


    def stare_at(self, trace_pos=None):
        if trace_pos == None:
            pass      
        else:
            x = int(trace_pos[0]+trace_pos[2]/2)
            y = int(trace_pos[1]+trace_pos[3]/2)
            x = int(240+(x-240)/4)
            y = int(160+(y-160)/1.6)
            self.move_flag = True
            self.eye_move_interpole(x,y)
            self.move_flag = False

    def change_mood(self, mood):
        if mood == 'angry' or mood == 0:
            self.artist.mood = self.angry
            self.angle = random.randrange(self.angry_angle[0], self.angry_angle[1])
            self.blink()
        elif mood == 'neutral' or mood == 1:
            self.artist.mood = self.neutral
            self.angle = 0
            self.blink()
        elif mood == 'sad' or mood ==2:
            self.angle = random.randrange(self.sad_angle[0], self.sad_angle[1])
            self.artist.mood = self.sad
            self.blink()
        elif mood == 'happy' or mood ==3:
            self.angle = 0
            self.artist.mood = self.happy
            self.blink()
        
    def update(self):
        # self.lock.acquire()
        # print("jump in update")
        self.img = self.img*0
        if self.artist.mood == self.happy:
            self.artist.make_happy(self.img, self.left_eye_size[0], self.left_eye_size[1], (self.left_eye[0], self.left_eye[1]), angle=self.angle)
            self.artist.make_happy(self.img, self.right_eye_size[0], self.right_eye_size[1], (self.right_eye[0], self.right_eye[1]), angle=-self.angle)
        elif self.artist.mood == self.angry:
            self.artist.make_angry(self.img, self.left_eye_size[0], self.left_eye_size[1]-self.angry_neg_height, (self.left_eye[0], self.left_eye[1]+10), angle=self.angle)
            self.artist.make_angry(self.img, self.right_eye_size[0], self.right_eye_size[1]-self.angry_neg_height, (self.right_eye[0], self.right_eye[1]+10), angle=-self.angle)
        else:
            self.artist.drawRoundRectangle(self.img, self.left_eye_size[0], self.left_eye_size[1], self.left_eye, angle=self.angle)
            self.artist.drawRoundRectangle(self.img, self.right_eye_size[0], self.right_eye_size[1], self.right_eye, angle=-self.angle)
        print("X: {}      Y:{}".format((self.left_eye[0]+self.right_eye[0])/2, (self.left_eye[1]+self.right_eye[1])/2))
        cv2.imshow("test", self.img)


"""
a = Move()
i=170
back = False
def test():
    global back
    i = 190
    while i<=420:
        # max range X is (190, 290)
        # max range Y is (90, 230 )
        trace_pos = (i, i/2) if back else (i, 2*i/3)
        # trace_pos = (random.randrange(110,390), random.randrange(90,210))
        # print(trace_pos)
        # if a.eyestrain():
            # a.blink()
        # a.change_mood(3) if i<=150 or i>=300 else 0
        
        # a.change_mood(random.randrange(0,4)) if i<=190 or i>=290 else 0
        # sleep (1)
        a.stare_at(trace_pos=trace_pos)
        # sleep (1.5)
        # sleep(1)

        # a.update()
        if i<=90:
            back = False
            sleep(1.02)
            a.move_flag = False
        elif i>=390:
            back=True
            sleep(1.53)
            a.move_flag = False
        if not back:
            i+=20
        else:
            i-=20
        if cv2.waitKey(5) == 27:
            break
test()
"""



