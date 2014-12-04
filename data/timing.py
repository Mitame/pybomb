import threading
import time
import data.settings as settings

class Queue(list):
    class Item():
        def __init__(self,target,atTick):
            self.target = target
            self.atTick = atTick
            
    
    def __init__(self):
        self.tick = 0
        self.tickerThread = threading.Thread(target=self.ticker)
        self.tickerThread.start()
        
    def add(self,target,atTick):
        self.append(self.Item(target,atTick))
        try:
            self.sort(key=self._getTick)
        except:
            pass
    
    def _getTick(self,item):
        return item.atTick
    
    def ticker(self):
        
        while settings.running:
            start = time.time()
            self.tick += 1
            for item in self:
                if item.atTick <= self.tick:
                    threading.Thread(target = item.target()).start()
                    try:
                        self.remove(item)
                    except:
                        pass
                else:
                    break
            wait = 1/settings.tickPerSec-time.time()+start
            if wait > 0:
                time.sleep(wait)
            else:
                print("Ticker Slow,",-wait,"s missed")
        print("Ending Ticker Thread")

queue = Queue()


def printTick():
    print("Tick:",activeQ.tick)


def test():
    global activeQ
    activeQ = Queue()
    for x in range(0,11,5):
        activeQ.add(printTick,x)
    activeQ.add(printTick,20)
    settings.close()

