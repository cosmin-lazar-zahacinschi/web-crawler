from threading import Thread, Condition, Timer, Lock
from crawl import log
from persistency import persistency

class Graph(Thread):
    
    edgeCount = dict()
    
    msgQueue = []
    isRunning = False
    update_timer_started = False
    
    def __init__(self):
        super().__init__()
        self.condition = Condition()
    
    def add_connection(self, from_url, to_url):
        self.condition.acquire()
        self.msgQueue.append((from_url, to_url))
        self.condition.notifyAll()
        self.condition.release()
    
    def start(self):
        self.isRunning = True
        Thread.start(self)
        
    def run(self):
        while self.isRunning == True:
            self.condition.acquire()
            while (len(self.msgQueue) < 1):
                self.condition.wait()
            
            msg = self.msgQueue.pop()
            self.condition.release()
            
            if msg != None:
                if (not msg in self.edgeCount):
                    self.edgeCount[msg] = 1
                else:
                    self.edgeCount[msg] = self.edgeCount[msg] + 1
                
                if self.update_timer_started == False:
                    t = Timer(5.0, self.do_update)
                    t.start()
                    self.update_timer_started = True
    
    def do_update(self):
        self.condition.acquire()
        persistency.add_connections(self.edgeCount)
        self.edgeCount.clear()
        self.update_timer_started = False
        self.condition.release()