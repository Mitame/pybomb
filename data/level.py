import pygame.sprite
import pygame.font
import random
from data import *
import data.generate as generate
import data.entities as entities
# import block
# import settings

class Map(pygame.sprite.Group):
    class type():
        classic = 0
        empty = 1
    def __init__(self,parent):
        pygame.sprite.Group.__init__(self)
        parent[type(self)] = self
        
        self.parent = parent
        self.rect = pygame.Rect(texture.bgPadding[:2],tuple(settings.gridSize[x] * settings.mapSize[x] for x in range(2)))
        self.type = self.parent.ltype
        self.gridSize = self.parent.gridSize
        self.spawnAreas = settings.levelGen.spawnAreas
         
    def generate(self):
        generate.level.generate(self,settings.levelGen.type)


class entLayer(Map):
    def __init__ (self,baseLevel):
        pygame.sprite.Group.__init__(self)
        self.grid = generate.grid(baseLevel.grid.size)
        self.gridSize = baseLevel.gridSize
        self.baseLevel = baseLevel
        self.parent = self.baseLevel.parent
        self.rect = pygame.Rect(texture.bgPadding[:2],tuple(settings.gridSize[x] * settings.mapSize[x] for x in range(2)))
        self.parent[type(self)] = self
    
    def runOnSprites(self,function,sprType = None,*args,**kwargs):
        for spr in self.sprites():
            if sprType is None or sprType == type(spr):
                function(spr,*args,**kwargs)

class playerLayer(entLayer):
    
    def __init__ (self,ents):
        entLayer.__init__(self, ents.baseLevel)
        self.entLayer = ents
        self.parent[type(self)] = self
        
    def spawnPlayer(self,spawnPoint = None):
        if spawnPoint == None:
            spawn = self.getSpawnSpot()
        else:
            spawn = self.baseLevel.spawnAreas[spawnPoint]
        
        self.grid.set(spawn,entities.player(self),False)
        self.grid.get(spawn).gridPos = spawn
        self.grid.get(spawn).genRect()
        print(len(self.spritedict))
        if len(self.spritedict) == 1:
            self.userPlayer = self.grid.get(spawn)
        return self.userPlayer
    
    def getSpawnSpot(self):
        return settings.levelGen.spawnAreaChance.getChoice()
    


class GUI(pygame.sprite.Group):
    class Mouse(pygame.sprite.Sprite):
        def __init__(self,*containers):
            pygame.sprite.Sprite.__init__(self,*containers)
            self.parent = containers[0]
            self.rect = pygame.Rect(0,0,0,0)
            self.image = pygame.Surface((1,1),pygame.SRCALPHA)
    
        def update(self,motion = False):
            if motion:
                event = pygame.event.get(pygame.MOUSEMOTION)[-1]
                self.rect.topleft = event.pos
            
            for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
                collisions = pygame.sprite.spritecollideany(self, self.parent)
                if type(collisions) in (list,tuple):
                    for x in collisions:
                        try:
                            x.onClick(event)
                        except AttributeError:
                            print("Item has no function 'onClick'")
                elif collisions is not None:
                    try:
                        collisions.onClick(event)
                    except AttributeError:
                        print("Item has no function 'onClick'")
    
    def __init__(self,parent):
        pygame.font.init()
        pygame.sprite.Group.__init__(self)
        font = pygame.font.SysFont("Ubuntu", 12)
        self.parent = parent
        self.parent[type(self)] = self
        self.layouts = {}
        
#     def showText(self,position,text):
#         sprite = pygame.sprite.Sprite(self)
#         sprite.image = pygame.Surface(self.font.size(text),pygame.SRCALPHA,32)
#         sprite.rect = sprite.image.get_rect(topleft = position)
    
    def addLayout(self,layout,name = None):
        x = layout(self)
        self.add(x)
        if name:
            self.layouts[name] = x
        else:
            self.layouts[str(x)] = x
        
    def removeLayout(self,layoutName):
        if layoutName in self.layouts:
            for spr in self.layouts[layoutName]:
                spr.kill()
            self.layouts.__delitem__(layoutName)
    
    def toggleLayout(self,layout, name):
        if name in self.layouts:
            self.removeLayout(name)
        else:
            self.addLayout(layout,name)
    
    
    def manageClicks(self):
        try:
            self.mouse
        except:
            self.mouse = GUI.Mouse(self)
        
        self.mouse.update(pygame.event.peek(pygame.MOUSEMOTION))


class groupContainer(dict):
    
    def __init__ (self,ltype):
        self.ltype = ltype
        self.gridSize = settings.gridSize
    
        
class extraMap(Map):
    
    def __init__(self,groupContainer):
        Map.__init__(self,groupContainer)
        self.mimic = self.parent[Map]
        self.grid = generate.grid(settings.mapSize)
        for blk in self.mimic.grid._map:
            if type(blk) not in (block.unbreakable,block.breakable):
                continue
            x = block.extra(parent = self, gridpos = blk.gridPos, blockToMimic = blk)
            self.add(x)
            
def test():
    import data.render
    level = groupContainer(Map.type.empty)
    l = Map(level)
    l.generate()
    ents = entLayer(l)
    players = playerLayer(ents)
    players.spawnPlayer()
    level[GUI] = GUI(level)
    if texture.extraOnBlocks:
        level[extraMap] = extraMap(level)
    data.control.withPlayers(level)

if __name__ == "__main__": test()