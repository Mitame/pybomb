import pygame.sprite, pygame.surface
import data.settings as settings
import data.textures as texture
from data import *
import data
import random

class Block(pygame.sprite.Sprite):
    density = 0
    def __init__(self,parent=None):
        if parent is not None:
            pygame.sprite.Sprite.__init__(self,parent)
        else:
            pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        
#         self.genImage()
        self.image = pygame.Surface((0,0))
        self.rect = self.image.get_rect(topleft = (16,16))
    
    def draw(self,surface):
        surface.blit(self.image,self.rect)
    
    def update(self,rect=False,image=False):
        if rect: self.genRect()
        if image: self.genImage()
        
    def genImage(self):
        self.image = pygame.surface.Surface((0,0))
    
    def genRect(self):
        try:
            temp = self.gridPos
        except:
            temp = (0,0)
        self.gridPos = self.parent.grid.find(self)
        if self.gridPos is not None:
            self.rect = self.image.get_rect(bottomright=tuple(self.gridPos[x]*self.parent.gridSize[x]+self.parent.rect.topleft[x] for x in range(2)))
        else:
            self.gridPos = temp
            self.rect = self.image.get_rect(bottomright=tuple(self.gridPos[x]*self.parent.gridSize[x] for x in range(2)))
        
        return self.rect
#         if self.parent.grid.find(item=self) == (1,1):
#             print(type(self), self.parent.grid.find(item=self))
#             self.image = pygame.Surface((16,16))
#             self.image.fill((255,255,255))


class empty(Block):
    density = 0
    def genImage(self):
#         try:
        if sum(self.gridPos) % 2 == 0:
            if self.gridPos[0] == 0:
                self.image = texture.block.empty4
            else:
                self.image = texture.block.empty0
        else:
            if self.gridPos[0] == 0:
                self.image = texture.block.empty3
            elif type(self.parent.grid.get((self.gridPos[0]-1,self.gridPos[1]))) == unbreakable:
                self.image = texture.block.empty2
            else:
                self.image = texture.block.empty1
#         except:
#             self.image = texture.block.empty

class breakable(Block):
    density = 1
    def genImage(self):
        self.image = texture.block.breakable
    
    def destroy(self):
        pos = self.parent.grid.find(self)
        self.parent.grid.set(pos,empty(self.parent),False)
        self.parent.grid._map[self.parent.grid._conv(p=pos)].genRect()
        self.parent.grid._map[self.parent.grid._conv(p=pos)].genImage()
        self.kill()
        
class unbreakable(Block):
    density = 2
    def genImage(self):
        self.image = texture.block.unbreakable

class spawn(empty):
    pass

class extra(Block):
    
    def __init__(self,parent = None,gridpos = None, blockToMimic = None):
        Block.__init__(self,parent)
        self.gridPos = gridpos
        self.blockToMimic = type(blockToMimic)
        self.parent.grid.set((self.gridPos),self,False)
        self.genRect()
        self.genImage()
        
    def genImage(self):
        if self.blockToMimic == unbreakable:
            self.image = texture.block.extra.unbreakable
        elif self.blockToMimic == breakable:
            self.image = texture.block.extra.breakable
        else:
            self.kill()
        
    def genRect(self,set = True):
#         result = (10,10)
        result = tuple(Block.genRect(self)[x]+(0,-settings.gridSize[1])[x]*0.25 for x in range(2))
        if set:
            self.rect = result
        return result
    
    def update(self):
        if not type(self.parent.mimic.grid.get(self.gridPos)) == self.blockToMimic:
            self.kill()

class conveyor(Block):
    
    def __init__(self,parent=None,dir="D"):
        Block.__init__(self,parent)
        self.dir = dir
    
    def genImage(self):
        self.image = pygame.Surface(settings.gridSize)
        self.image.fill((255,0,255))
        
def emptyOrBreakable(parent=None):    
    x = random.randint(0,100)
    if x< settings.levelGen.blockEmpty:
        return empty(parent)
    else:
        return breakable(parent)
        
    
def test():
    import data.render
    temp = breakable()
    temp.genImage()
    temp.rect = pygame.Rect(16,16,16,16)
    data.render.staticSprite(temp)


if __name__ == "__main__": test()