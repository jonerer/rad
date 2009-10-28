import threading
import thread
import time

class Trad(threading.Thread):
    def __init__(self, msg):
        super(Trad, self).__init__()
        self.weo = msg

    def run(self):
        print "klink", self.weo

def thr(a, b):
    print "klonk:", a, b

a = Trad(55)
a.start()
thread.start_new_thread(thr, (3, 1))
