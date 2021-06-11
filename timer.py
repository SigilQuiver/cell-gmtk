import math


def int_tuple(vector):
    return (int(vector[0]), int(vector[1]))


class Timer:
    def __init__(self, time):
        self.max_time = time
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt / 1000
        if self.current_time >= self.max_time:
            self.current_time = 0
            return True
        return False


def lerp(p1,p2,perc):
    return p1 + (p2 - p1) * perc


def quadratic(x):
    return x * x


def cubic(x):
    return x * x * x


def quadratic_in_out(x):
    if x < 0.5:
        return 2 * x * x
    else:
        return -1 + (4 - 2 * x) * x


def cos_back(x):
    return -(math.cos(2*x*math.pi)/2)+0.5


class TimerLerp:
    def __init__(self,time,v1,v2):
        self.max_time = time
        self.current_time = 0
        self.max_val = v2
        self.min_val = v1
        self.current_val = v1
        self.lerp_progress = 0

    def update(self,dt,func=None):

        self.lerp_progress = self.current_time/self.max_time
        if self.current_time < self.max_time:
            self.current_time += dt / 1000
        else:
            self.lerp_progress = 1

        if func == None:
            self.current_val = lerp(self.min_val,self.max_val,self.lerp_progress)
        else:
            self.current_val = lerp(self.min_val, self.max_val, func(self.lerp_progress))

        return self.current_val


def work_timer(dt,v1,v2,timer,time=1,func=quadratic_in_out):
    if timer == None and v1 != v2:
        timer = TimerLerp(time,v1,v2)
    if timer != None:
        v1 = timer.update(dt, func)
        if v1 == v2 or v2 != timer.max_val:
            timer = None
    return v1,timer
