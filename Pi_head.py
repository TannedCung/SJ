import wiringpi2 as wiringpi         # Import Wiringpi module
from time import sleep  # Import sleep from time module
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
        self.v_deg = 0
        self.v_deg_range = [0,60]
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
        wiringpi.pwmWrite(self.horizon_pin, self.interp(h_deg))
        wiringpi.pwmWrite(self.vertical_pin, self.interp(v_deg))
        sleep(self.delay)

    def face_trace(self, cx, cy):
        if cx > self.frame_cx and self.in_range(self.h_deg, self.h_deg_range):
            self.h_deg = self.h_deg + 1
        elif cx > self.frame_cx and self.in_range(self.h_deg, self.h_deg_range):
            self.h_deg = self.h_deg - 1
        if cy > self.frame_cy and self.in_range(self.v_deg, self.v_deg_range):
            self.v_deg = self.v_deg + 1
        elif cy > self.frame_cy and self.in_range(self.v_deg, self.v_deg_range):
            self.v_deg = self.v_deg - 1
        self.move(h_deg=self.h_deg, v_deg=self.v_deg)