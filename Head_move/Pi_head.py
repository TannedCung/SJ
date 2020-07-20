import wiringpi         # Import Wiringpi module
from time import sleep  # Import sleep from time module
from PID_test import *
# import random

class Head_move():
    def __init__(self):
        self.pw_range = [50, 255]
        self.frame_cx = (480/2)
        self.frame_cy = (320/2)
        self.horizon_pin = 18
        self.vertical_pin = 19
        self.delay = 0.005 
        self.h_deg_range = [0,180]
        self.h_deg = 90
        self.v_deg = 30
        self.v_deg_range = [0,60]
        self.captainx = cal_PID()
        self.captainy = cal_PID()
        # set up servo paramater
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.horizon_pin, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pinMode(self.vertical_pin, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)

        self.move(h_deg=self.h_deg, v_deg=self.v_deg)

    def in_range(self, value, value_range):
        mi = value_range[0]
        ma = value_range[1]
        if value >= mi and value <= ma:
            return 1
        else:
            return 0 


    def interp(self, deg):
        pw = deg*(self.pw_range[1] - self.pw_range[0])/180 + self.pw_range[0]
        return int(pw)

    def move(self, h_deg, v_deg):
        print ("h={},     v={}".format(h_deg, v_deg))
        wiringpi.pwmWrite(self.horizon_pin, self.interp(h_deg))
        wiringpi.pwmWrite(self.vertical_pin, self.interp(v_deg))
        sleep(self.delay)
        
    def cal_err(self, cx, cy, w):
        x_err = abs(self.frame_cx - cx)
        y_err = abs(self.frame_cy - cy)
        ry = self.captainy.cal(y_err, w)
        rx = self.captainx.cal(x_err, w)
        return rx, ry


    def trace(self, pos):
        x, y, w, h = pos
        cx = int(x+w/2)
        cy = int(y+h/2)
        rx, ry = self.cal_err(cx, cy, w)
        # print ("rx: {:.2f}   ry: {:.2f}". format(rx, ry))
        
        if cx-self.frame_cx >= w/8 and self.in_range(self.h_deg+rx, self.h_deg_range):
            self.h_deg = self.h_deg + rx
        elif self.frame_cx-cx > w/8 and self.in_range(self.h_deg-rx, self.h_deg_range):
            self.h_deg = self.h_deg - rx
        if cy-self.frame_cy >=w/12 and self.in_range(self.v_deg-ry, self.v_deg_range):
            self.v_deg = self.v_deg - ry
        elif self.frame_cy -cy > w/12 and self.in_range(self.v_deg+ry, self.v_deg_range):
            self.v_deg = self.v_deg + ry
        self.move(h_deg=self.h_deg, v_deg=self.v_deg)
        
    