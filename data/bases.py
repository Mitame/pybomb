import random
import data

class Powerups():
    maxSpeed = 10
    speed = 1 if not data.settings.gameplay.maxPowerup else maxSpeed 
    maxPower = 10
    power = 1 if not data.settings.gameplay.maxPowerup else maxPower
    maxBombs = 10
    bombs = 1 if not data.settings.gameplay.maxPowerup else maxBombs 
    bombsRemaining = bombs
    bombsPlaced = 0
    
    
    piercing = False if not data.settings.gameplay.maxPowerup else True
    kick = False if not data.settings.gameplay.maxPowerup else True
    
    diahhorea = False
    
    invulnerable = False
    collected = []
    def __str__(self):
        return str("Speed:"+str(self.speed)+"\nPower:"+str(self.power)+"\nBombs"+str(self.bombs)+"\nPiercing:"+str(self.piercing)+"\nKick"+str(self.kick))

class randomChoice():
    def __init__(self):
        self.outcomes = []
    
    def getChoice(self,seed=None):
        if seed == None:
            seed = random.randint(0,len(self.outcomes)-1)
        if seed < len(self.outcomes):
            return self.outcomes[seed]
        else:
            return None
    
    def addChoice(self,result, chance):
        self.outcomes.extend([result for x in range(chance)])
    
    def remChoice(self,result):
        while self.outcomes.count(result) != 0:
            self.outcomes.remove(result)
    def getTotalChance(self):
        return len(self.outcomes)

class cheats():
    
    def __init__(self):
        self.keypresses = ""
        self.cheatList = {}
    def update(self, showMessage = False, gui = None):
        for x in self.cheatList.keys():
            if self.keypresses[-len(x):] == x:
                cheat = self.cheatList[x]
                if cheat[4]:
                    cheat[1](*cheat[2],**cheat[3])
                    self.keypresses = ""
                    if showMessage:
                        if gui:
                            x = data.gui.baseGUIItems.TextBox(gui, absPos = (15,15), text = "Cheat Activated: "+cheat[0])
                            data.timing.queue.add(x.kill, data.timing.queue.tick+data.settings.tickPerSec*5)
                        else:
                            print("Cheat Activated: "+cheat[0])
    def addCheat(self,code, name, target,*args,**kwargs):
        self.cheatList[code] = [name,target,args,kwargs,True]
    
    def removeCheat(self,code):
        if code in self.cheatList:
            self.cheatList[code][3] = False
    
    