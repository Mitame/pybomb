'''
Created on 10 May 2014

@author: Levi Wright
'''

import pygame.sprite
import data.textures as texture
import data.timing as timing
import data.settings as settings
import data.block as block
import data.bases as bases
import copy
import random

class base(pygame.sprite.Sprite):
    offsets = {"U":(0,-1),"D":(0,1),"L":(-1,0),"R":(1,0)}
    
    def genRect(self,gridPos=None,retr = False): 
        if gridPos == None:
            gridPos = self.parent.grid.find(self)
            retr = False
#             if gridPos == False:
#                 print(self.parent.grid)
        else:
            retr = True
        rect = self.image.get_rect(bottomleft=tuple((gridPos[x]+(0,1)[x])*self.parent.gridSize[x]+self.parent.rect.topleft[x]+self.additional[x] for x in range(2)))
        temp = tuple(gridPos[x]%1 >= 0.5 for x in range(2))
        gridPos = tuple(int(gridPos[x]) + int(temp[x]) for x in range(2)) 
        if retr == True:
            return rect,gridPos
        else:
            try:
                self.rectList.append((rect,gridPos))
            except:
                self.rect = rect
                self.gridPos = gridPos
    
    def move(self,relative,smooth = True,overFrames = 0):
        self.moving = True
        if not smooth:
            self.rectList.append(self.genRect(tuple(self.gridPos[x]+relative[x] for x in range(2))))
        elif smooth:
            frames = max(overFrames,1)
            if settings.gameplay.lockToGrid:
                start = self.rectList[-1][1]
                for x in range(frames):
                    x += 1
                    self.rectList.append(self.genRect(tuple(start[i]+relative[i]*(x/frames) for i in range(2)), True))
            else:
                start = self.rectList[-1][1]
                self.rectList.append(self.genRect(tuple(start[i]+relative[i]*(1/frames) for i in range(2)), True))
        return True
    
class bomb(base):
    name = "Bomb"
    additional = (0,0)
    def __init__(self, container,placer = None,spawntick=None):
        base.__init__(self,container)
        self.rect = pygame.Rect(0,0,0,0)
        self.gridPos = None
        self.placer = placer
        self.image = texture.entities.bomb0
        self.timer = 0
        self.altImg = False
        self.parent = container
        self.rectList = []
        #add queue items
        if spawntick is not None:
            s = spawntick
        else:
            s = timing.queue.tick
        for x in (5,5,5,5,4,4,4,4,3,3,3,3,2,2,2,2,1,1,1,1,1,1,1,1,1,1):
            s += x
            timing.queue.add(self.tick, s)
        timing.queue.add(self.explode, s+1)
        
        if self.placer is not None:
            self.powerups = copy.copy(self.placer.powerups)
        
        self.moving = False
        
    def tick(self):
        self.altImg = not self.altImg
        
#         if self.altImg:
#             self.image = texture.entities.bomb1
#         else:
#             self.image = texture.entities.bomb0
        if self.altImg:
            self.image = texture.entities.bomb1
        else:
            self.image = texture.entities.bomb0
        
    def explode(self):
        if not self.alive():
            return
        if self.placer is not None:
            self.placer.powerups.bombsPlaced -= 1
        self.kill()
        pos = self.gridPos
        tick = copy.copy(timing.queue.tick)
        
        dirs = [[1,0,False],[0,1,False],[-1,0,False],[0,-1,False]]
        for dist in range(1,self.powerups.power+1):
            for offset in dirs:
                if offset[2]:
                    continue
                bpos = tuple(pos[x]+(offset[x]*dist) for x in range(2))
                hit = False
                if not (settings.mapSize[0] > bpos[0] >= 0) or not (settings.mapSize[1] > bpos[1] >= 0):
                    dirs[dirs.index(offset)][2] = True
                    continue
                
                if type(self.parent.grid.get(bpos)) == bomb:
                    self.parent.grid._map[self.parent.grid._conv(p=bpos)].explode()
                
#                 if type(self.parent.grid.get(bpos)) == blast and self.parent.grid.get(bpos).alive():
#                     dirs[dirs.index(offset)][2] = True
#                     print(bpos)
#                     continue
                
                if type(self.parent.baseLevel.grid.get(bpos)) == block.unbreakable:
                    dirs[dirs.index(offset)][2] = True
                    continue
                elif type(self.parent.baseLevel.grid.get(bpos)) == block.breakable:
                    self.parent.baseLevel.grid._map[self.parent.baseLevel.grid._conv(p=bpos)].destroy()
                    if not self.powerups.piercing:
                        dirs[dirs.index(offset)][2] = True
                    hit = True 


                self.parent.grid.set(bpos,blast(self.parent,tick,hit,owner = self.placer))
                self.parent.grid._map[self.parent.grid._conv(p=bpos)].genRect()
        self.parent.grid.set(pos,blast(self.parent,tick,owner = self.placer))
        self.parent.grid._map[self.parent.grid._conv(p=pos)].genRect()
        self.parent.update()
    
    def push(self,direction):
        offset = self.offsets[direction]
        self.moving = True
        dist = 1
        while True:
            resultPos = tuple(self.gridPos[x]+offset[x]*dist for x in range(2))
            if self.parent.grid.within(resultPos):
                if self.parent.baseLevel.grid.get(resultPos).density == 0 and type(self.parent.grid.get(resultPos)) != bomb:
                    print(dist, resultPos)
                    dist += 1
                else:
                    break
            else:
                break
        
        speed = settings.gameplay.bombSpeed
        if speed == -1:
            speed = self.placer.powerups.maxSpeed -self.placer.powerups.speed
        print(speed)
        self.move(tuple(offset[x]*(dist-1) for x in range(2)), overFrames = dist*speed)
        
    def update(self):
        try:
            self.rect,gridPos = self.rectList.pop(0)
            if gridPos != self.gridPos:
                if self.gridPos != None:
                    self.parent.grid.move(self.gridPos,gridPos,killNew = True)
                self.gridPos = gridPos
        except: pass
        
        if len(self.rectList) == 0:
            self.rectList.append((self.rect,self.gridPos))
            self.moving = False

class blast(base):
    name = "bomb blast"
    additional = (0,0)
    def __init__(self, container,spawnTick, drop = False, owner = None):
        pygame.sprite.Sprite.__init__(self,container)
        self.rect = pygame.Rect((0,0),settings.gridSize)
        self.image = pygame.Surface(settings.gridSize)
        self.gridPos = None
        self.timer = 0
        self.owner = owner
        self.dropBomb = drop
        self.animTick = -1
        self.parent = container
        self.image = pygame.Surface(settings.gridSize)
        #add queue items
        s = spawnTick
        for x in (1,2,2,1):
            s += x*3
            timing.queue.add(self.tick, s)
        timing.queue.add(self.burnOut, s+1)
    def tick(self):
        self.animTick += 1
        
        try:
            x = self.imageSet[self.animTick]
            self.image = x
        except:
            pass

    def burnOut(self):
        if self.dropBomb:
            drop = settings.dropChance.getChoice()
            if drop != None:
                self.parent.grid.set(self.gridPos,drop(self.parent))
                self.parent.grid.get(self.gridPos).genRect()
            
        self.kill()
        # cause entities around it to update
        for offset in [[1,0,False],[0,1,False],[-1,0,False],[0,-1,False]]:
            try:
                self.parent.grid.get((self.gridPos[x]+offset[x] for x in range(2))).update()
            except:
                pass
        
    def loadImage(self):
        if self.type == "R":
            self.imageSet = texture.blast.R
        elif self.type == "D":
            self.imageSet = texture.blast.D
        elif self.type == "L":
            self.imageSet = texture.blast.L
        elif self.type == "U":
            self.imageSet = texture.blast.U
            
        elif self.type == "RL":
            self.imageSet = texture.blast.RL
        elif self.type == "DU":
            self.imageSet = texture.blast.DU
        
        elif self.type == "RU":
            self.imageSet = texture.blast.RU
        elif self.type == "RD":
            self.imageSet = texture.blast.RD
        elif self.type == "DL":
            self.imageSet = texture.blast.DL
        elif self.type == "LU":
            self.imageSet = texture.blast.LU
        
        elif self.type == "RLU":
            self.imageSet = texture.blast.RLU
        elif self.type == "RDU":
            self.imageSet = texture.blast.RDU
        elif self.type == "RDL":
            self.imageSet = texture.blast.RDL
        elif self.type == "DLU":
            self.imageSet = texture.blast.DLU
            
        elif self.type == "ALL":
            self.imageSet = texture.blast.ALL
        else:
            self.kill()
            return
        self.image = self.imageSet[self.animTick]
        
    def update(self):
        result = []
        pos = self.parent.grid.find(self)
        if type(pos) is not bool:
            for offset in ((1,0),(0,1),(-1,0),(0,-1)):
                checkpos = tuple(pos[x]+offset[x] for x in range(2))
                if self.parent.grid.within(checkpos):
                    item = self.parent.grid.get(checkpos)
                    if type(item) == blast and item.alive():
                        result.append(True)
                    else:
                        result.append(False)
                else: result.append(False)
            if all(result):
                self.type = "ALL"
            else:
                self.type = ""
                for x in range(4):
                    if result[x]:
                        self.type += "RDLU"[x]
            self.loadImage()
        else:
            self.kill()
class world():
    name = "the World"
    powerups = bases.Powerups()
class player(base):
    name = settings.playerName
    additional = texture.player.additional
    def __init__(self,container=None):
        base.__init__(self,container)
        self.animFrame = -1
        self.animIndex = 0
        self.parent = container
        self.living = True
        self.set_imageSet("D")
        
        self.gridPos = None
        self.image = self.imageSet[0]
        self.rectList = []
        self.powerups = bases.Powerups()
        self.moving = False
        self.name = settings.playerName
        

        
    def respawn(self, atSpawnPoint = True):
        self.add(self.parent)
        if atSpawnPoint:
            x = settings.levelGen.spawnAreaChance.getChoice()
            self.parent.grid.move(self.gridPos, x)
            self.rectList = [self.genRect(x,True)]
        self.living = True
        self.set_imageSet()
        self.powerups = bases.Powerups()
        if settings.visuals.hideHUDonDeath:
            import data.level as level
            import data.gui as gui
            self.parent.parent[level.GUI].toggleLayout(gui.playerStats,"mainPlayerStats")
        
    def collect(self,item):
        if not self.living:
            return False
        itype = type(item)
        if itype in vars(powerups).values() and (item.alive() or item.dummy):
            if itype == powerups.bombup:
                self.powerups.bombs = min(self.powerups.maxBombs,self.powerups.bombs+1)
                self.powerups.bombsRemaining = min(self.powerups.maxBombs,self.powerups.bombsRemaining+1)
            elif itype == powerups.kick:
                self.powerups.kick = True
            elif itype == powerups.piercing:
                self.powerups.piercing = True
            elif itype == powerups.powerup:
                self.powerups.power = min(self.powerups.maxPower,self.powerups.power+1)
            elif itype == powerups.speedup:
                self.powerups.speed = min(self.powerups.maxSpeed,self.powerups.speed+1)
            
            elif itype == powerups.bombdown:
                if self.powerups.bombs != 1:
                    self.powerups.bombsRemaining -= 1
                self.powerups.bombs = max(1,self.powerups.bombs - 1)
            elif itype == powerups.kickoff:
                self.powerups.kick = False
            elif itype == powerups.piercingoff:
                self.powerups.piercing = False
            elif itype == powerups.powerdown:
                self.powerups.power = max(1,self.powerups.power - 1)
            elif itype == powerups.speeddown:
                self.powerups.speed = max(1,self.powerups.speed - 1)
            
            elif itype == powerups.diarrhea:
                self.powerups.diahhorea = True
            elif itype == powerups.cure:
                self.powerups.diahhorea = False
            
            elif itype == powerups.invulnerable:
                self.powerups.invulnerable = True
            if not item.dummy:
                self.powerups.collected.append(itype)
            item.kill()
        
    def update(self):
        if self.moving:
            self.animIndex += self.powerups.speed*texture.player.animSpeedMultiplyer
            if self.animIndex >= texture.player.animFrames:
                self.animFrame += 1
                self.animIndex = 0
                self.image = self.imageSet[texture.player.animOrder[self.animFrame%len(texture.player.animOrder)]]
        else:
            self.image = self.imageSet[texture.player.animIdle]
            self.animFrame = 0
        
        try:
            self.rect,gridPos = self.rectList.pop(0)
            if gridPos != self.gridPos:
                if self.gridPos != None:
                    self.parent.grid.move(self.gridPos,gridPos,killNew = False)
                self.gridPos = gridPos
        except: pass
        if len(self.rectList) <= 1:
            self.moving = False
        if len(self.rectList) == 0:
            self.rectList.append((self.rect,self.gridPos))

        if self.living and self.alive():
            self.collect(self.parent.entLayer.grid.get(self.gridPos)) 
            beneath = self.parent.entLayer.grid.get(self.gridPos)
            if type(beneath) == blast and beneath.alive():
                self.kill(entity = beneath)
        
        self.manageAliments()
#     
        self.powerups.bombsRemaining = self.powerups.bombs - self.powerups.bombsPlaced
    def action(self,event=None,key = None,action = None):
        if not self.alive() and not settings.gameplay.ghosting:
            return False
        if event:
            action = settings.controls.player[event.key]
        elif key:
            action = settings.controls.player[key]
        elif action == None:
            return
        

        if action == "walkUp":
            self.set_imageSet("U")
            self.move((0,-1))
        elif action == "walkDown":
            self.set_imageSet("D")
            self.move((0,1))
        elif action == "walkLeft":
            self.set_imageSet("L")
            self.move((-1,0))            
        elif action == "walkRight":
            self.set_imageSet("R")
            self.move((1,0))
        elif action == "dropBomb" and self.living and self.alive() and not self.moving:
            self.dropBomb()
        elif action == "respawn" and not self.living:
            self.respawn()
            
    
    def manageAliments(self):
        if not (self.living or self.alive()):
            return
        if self.powerups.diahhorea:
            self.action(action="dropBomb")
#             self.oldSpeed = self.powerups.speed
#             self.powerups.speed = self.powerups.maxSpeed
            
    def kick(self):
        item = self.parent.entLayer.grid.get(tuple(self.gridPos[x]+self.offsets[self.dir][x] for x in range(2)))
        if type(item) == bomb and not item.moving:
            item.push(self.dir)
            
    def move(self,relative, smooth=True):
        if len(self.rectList) > 1:
            return
        
        resultPos = tuple(self.gridPos[x]+relative[x] for x in range(2))
        density = self.parent.baseLevel.grid.get(resultPos).density
        if density:
            if self.living or settings.gameplay.ghostMaxDensity < density:
                return
            
        ent = self.parent.entLayer.grid.get(resultPos)
        if type(ent) == bomb and ent.alive():
            if self.powerups.kick:
                self.kick()
            return False 
        
        if not self.parent.grid.within(resultPos):
            return False
        
        frames = int(((self.powerups.maxSpeed+1 - self.powerups.speed)/2)+settings.gameplay.baseMovementSpeed)
        base.move(self, relative, overFrames=frames)


    def dropBomb(self):
        if self.powerups.bombsRemaining > 0:
            beneath = self.parent.entLayer.grid.get(self.gridPos)
            if type(beneath) == bomb and beneath.alive():
                return
             
            x = bomb(self.parent.entLayer,self)
            self.parent.entLayer.grid.set(self.gridPos,x)
            x.genRect()
            x.update()
            if type(beneath) == blast and beneath.alive():
                x.explode()
            self.powerups.bombsPlaced += 1
        
    def kill(self, entity = None):
        if self.powerups.invulnerable:
            return
        if entity is not None:
            byPlayer = entity.owner.name if entity is not None else "The World"
            print("I've been killed by",byPlayer,"who used a",entity.name,"to kill me.")
        else:
            print("I've been killed")
        if settings.gameplay.deathDropPowerups:
            for p in self.powerups.collected:
                if random.randint(0,100) < settings.gameplay.deathDropChance:
                    x,y = (random.randint(0,settings.mapSize[x]) for x in range(2))
                    if not self.parent.baseLevel.grid.get((x,y)).density:
                        self.parent.entLayer.grid.set((x,y),p(self.parent.entLayer))
                        try:
                            self.parent.entLayer.grid.get((x,y)).genRect()
                        except: pass
                
        if settings.gameplay.ghosting:
            self.living = False
            self.powerups.speed = 10
            if settings.visuals.hideHUDonDeath:
                import data.level as level
                import data.gui as gui
                self.parent.parent[level.GUI].toggleLayout(gui.playerStats,"mainPlayerStats")
            
        else:
            base.kill(self)
        self.set_imageSet()

    def set_imageSet(self,direction=None):
        if direction==None:
            direction = self.dir
        else:
            direction = direction.upper()
            self.dir = direction
        if direction == "U":
            if self.living:
                self.imageSet = texture.player.U
            else:
                self.imageSet = texture.player.transparent.U
        elif direction == "D":
            if self.living:
                self.imageSet = texture.player.D
            else:
                self.imageSet = texture.player.transparent.D
        elif direction == "R":
            if self.living:
                self.imageSet = texture.player.R
            else:
                self.imageSet = texture.player.transparent.R
        elif direction == "L":
            if self.living:
                self.imageSet = texture.player.L
            else:
                self.imageSet = texture.player.transparent.L
        self.image = self.imageSet[texture.player.animOrder[self.animFrame%len(texture.player.animOrder)]]


class basePowerup(base):
    additional = (0,0)
    def __init__(self,parent=None,dummy = False):
        if not dummy:
            if parent is not None:
                base.__init__(self,parent)
            else:
                base.__init__(self)
            self.parent = parent
            self.genImage()
            self.rect = pygame.Rect((0,0),settings.gridSize)
            
        else:
            base.__init__(self)
        self.dummy = dummy

class powerups():
    class speedup(basePowerup):
        def genImage(self):
            self.image = texture.entities.speedup
    class piercing(basePowerup):
        def genImage(self):
            self.image = texture.entities.piercing
    class powerup(basePowerup):
        def genImage(self):
            self.image = texture.entities.powerup
    class bombup(basePowerup):
        def genImage(self):
            self.image = texture.entities.bombup
    class kick(basePowerup):
        def genImage(self):
            self.image = texture.entities.kick
    
    class speeddown(basePowerup):
        def genImage(self):
            self.image = texture.entities.speeddown
    class piercingoff(basePowerup):
        def genImage(self):
            self.image = texture.entities.piercingoff
    class powerdown(basePowerup):
        def genImage(self):
            self.image = texture.entities.powerdown
    class bombdown(basePowerup):
        def genImage(self):
            self.image = texture.entities.bombdown
    class kickoff(basePowerup):
        def genImage(self):
            self.image = texture.entities.kickoff
    
    class invulnerable(basePowerup):
        def genImage(self):
            self.image = pygame.Surface(settings.gridSize)
            self.image.fill((0,255,0))
    
    class diarrhea(basePowerup):
        def genImage(self):
            self.image = pygame.Surface(settings.gridSize)
            self.image.fill((255,0,0))
    
    class cure(basePowerup):
        def genImage(self):
            self.image = pygame.Surface(settings.gridSize)
            self.image.fill((0,255,0))
powerups.all = [powerups.speedup,powerups.piercing,powerups.powerup,powerups.bombup,powerups.kick]
        