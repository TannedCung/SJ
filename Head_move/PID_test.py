import time

class cal_PID():
    def __init__(self, Kp=60, Ki=0.5, Kd =0.5):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.pre_time = time.time()
        self.pre_err = 0
        self.Ci = 0
        self.Cd = 0
        self.Cp = 0
        
    def cal(self, err, w):
        self.w = w/2200
        self.err = err/240
        self.cur_time = time.time()
        dt = (self.cur_time - self.pre_time)
        self.pre_time = self.cur_time
        de = (self.err - self.pre_err)
        self.pre_err = self.err
        
        self.Cp = self.Kp*self.err*self.w
        self.Ci = self.Ci + self.w*self.err*dt
        self.Cd = 0
        if dt > 0:
            self.Cd = de/dt
        return self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)