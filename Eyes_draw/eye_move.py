from eye_draw import *
import cv2
import numpy as np
from time import sleep
import threading


class Move():
    def __init__(self):
        self.left_eye = (135,160)
        self.right_eye = (345,160)
        self.left_eye_size = (150, 150)
        self.right_eye_size = (150, 150)
        self.min_height = 50
        self.img = np.zeros((320,480,3), np.uint8)
        # cv2.imshow("test", self.img)
        self.blink_step = 5
        self.offset_step = 50
        # mood
        self.happy = (10,225,10)
        self.neutral = (225,225,10)
        self.angry = (50,50,225)
        self.artist = Draw(mood=self.neutral)
        self.max_offset = 50
        self.move_flag = False
        self.blink_flag = False
        self.lock = threading.Lock()
        # Threads
        # self.stare()
        """
        self.blink_thread = threading.Thread(target=self.blink)
        self.stare_at_thread = threading.Thread(target=self.stare_at)
        # self.stare_thread = threading.Thread(target=self.stare)
        self.blink_thread.daemon = True
        self.stare_at_thread.daemon = True
        # self.stare_thread.daemon = True
        self.blink_thread.start()
        self.stare_at_thread.start()
        # self.stare_thread.start()
        """

    def cal_widthNheight(self, offsetX, offsetY):
        # if offset>0 the eyes go to the right and vice versal
        if abs(offsetX) > self.max_offset:
            offsetX = int(self.max_offset*(offsetX/abs(offsetX)))
        if abs(offsetY) > self.max_offset:
            offsetY = int(self.max_offset*(offsetY/abs(offsetY)))
        print("offX:{}   offY:{}".format(offsetX,offsetY))
        self.left_eye = (135+offsetX, 160+offsetY)  
        self.right_eye = (345+offsetX, 160+offsetY)
        # recal the size
        self.left_eye_size = (int(150-offsetX*0.1*150/self.max_offset), int(150-(offsetX*0.15*150/self.max_offset)-(abs(offsetY)*0.15*150/self.max_offset)))
        self.right_eye_size = (int(150+offsetX*0.1*150/self.max_offset), int(150+(offsetX*0.15*150/self.max_offset)-(abs(offsetY)*0.15*150/self.max_offset)))
        
        # self.left_eye_size = (self.left_eye_size[0], 150-offsetY*0.2*150/self.max_offset)
        # self.right_eye_size = (self.right_eye_size[0], 150-offsetY*0.2*150/self.max_offset)

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
            # sleep(0.05)
            self.update()
            if self.blink_step>=5:
                openup = False
                done = True
                # sleep(1)
            elif self.blink_step <=1:
                openup = True
                # sleep(1)
            if cv2.waitKey(5) == 27:
                break
            # self.lock.release()

    
    def stare_at(self, trace_pos=None):
        if trace_pos == None:
            pass      
        else:
            # self.lock.acquire()
            # sleep(2)
            self.move_flag = True
            """
            steps =  int(abs(x-(self.left_eye[0]+self.right_eye[0])/2)/self.offset_step)
            for step in range(steps):
                self.left_eye[0] += self.offset_step
                self.right_eye[0] += self.offset_step
            """
            x, y = trace_pos
            """
            offsetX = int(x-(self.left_eye[0]+self.right_eye[0])/2)
            offsetY = int(y-(self.left_eye[1]+self.right_eye[1])/2)
            """
            offsetX = int((x-240)/2)
            offsetY = int((y-160)/2)
            self.cal_widthNheight(offsetX, offsetY)
            self.update()
            self.move_flag = False
            self.blink()
            # self.lock.release()

        
    def update(self):
        # self.lock.acquire()
        # print("jump in update")
        self.img = self.img*0
        self.artist.drawRoundRectangle(self.img, self.left_eye_size[0], self.left_eye_size[1], self.left_eye)
        self.artist.drawRoundRectangle(self.img, self.right_eye_size[0], self.right_eye_size[1], self.right_eye)
        # print("w: {}    h: {}".format(self.left_eye_size[0], self.left_eye_size[1]))       
        # print("-------")
        # cv2.line(self.img, (240,0), (240,320), (0,225,225))
        cv2.imshow("test", self.img)
        #sleep(0.001)
        #self.lock.release()

a = Move()
i=170
back = False
def test():
    global back
    i = 150
    while i<=410:
        # trace_pos = (75, -2*i) if back else (390,i)
        trace_pos = (random.randrange(0,480), random.randrange(0,320))
        # print(trace_pos)
        # a.blink()
        a.stare_at(trace_pos=trace_pos)  
        sleep(1)

        # a.update()
        if i<=170:
            back = False
            # sleep(5)
            a.move_flag = False
        elif i>=310:
            back=True
            # sleep(5)
            a.move_flag = False
        if not back:
            i+=240
        else:
            i-=240
        if cv2.waitKey(5) == 27:
            break
test()




