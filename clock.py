import datetime
import time
import threading

class Clock:

    # Initializing the clock with the system time
    def __init__(self, sys_time = datetime.datetime.now(), drift_rate = 1):
        self.local_time = sys_time
        self.t = threading.Thread(target = self.tick, args = (drift_rate, ))
        self.t.start()
    # Keeping the clock ticking at every millisecond with a specified drift rate [for simulation purposes]
    def tick(self, drift_rate = 1):
        while True:
            time.sleep(0.001)
            self.local_time = self.local_time + datetime.timedelta(seconds = drift_rate * 0.001)

    # Setting the local clock time [To be used for sync]
    def setTime(self, new_time):
        # self.local_time = self.local_time + datetime.timedelta(seconds = time_dif)
        self.local_time = new_time

    # Obtaining the local clock time
    def getTime(self):
        return self.local_time

    def __del__(self):
        self.t._stop()
