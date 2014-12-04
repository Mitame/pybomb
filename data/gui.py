import pygame
pygame.font.init()
from data import level,settings,textures,entities

                    
                      
class baseGUIItems():
    class base(pygame.sprite.Sprite):
        def __init__(self,parent,relPos = None, absPos = None,genImage = True):
            pygame.sprite.Sprite.__init__(self,parent)
            self.relative = relPos is not None
            self.pos = relPos if self.relative else absPos
            self.parent = parent
            self.image = pygame.Surface((128,128))
            self.genRect()
            if genImage:
                self.genImage()
        def genRect(self):
            if self.relative:
                self.rect = self.image.get_rect(topleft = tuple(self.pos[x] + self.parent.rect.topleft[x] for x in range(2)))
            else:
                self.rect = self.image.get_rect(topleft = self.pos)
        
        def genImage(self):
            self.image = pygame.Surface(20,20)
        
        def onClick(self,event):
            pass
        
    class Button(base):
        def genImage(self):
            bs = textures.gui.buttonSpacing
            if False:
                self.image = textures.rawTextures.gui
                return
            self.image = pygame.Surface(self.rect.size)
            relRect = self.image.get_rect()
            self.image.blit(textures.gui.TR[0], textures.gui.TR[0].get_rect(topright = relRect.topright))
            self.image.blit(textures.gui.RB[0], textures.gui.RB[0].get_rect(bottomright = relRect.bottomright))
            self.image.blit(textures.gui.BL[0], textures.gui.BL[0].get_rect(bottomleft = relRect.bottomleft))
            self.image.blit(textures.gui.LT[0], textures.gui.LT[0].get_rect(topleft = relRect.topleft))
            
            rect = textures.gui.T[0].get_rect(top = relRect.top,left = relRect.left+bs[1],w = relRect.w-bs[1]*2,h = bs[1])
            self.image.blit(pygame.transform.smoothscale(textures.gui.T[0],rect.size),rect)
            
            rect = textures.gui.R[0].get_rect(top = relRect.top+bs[1], right = relRect.right, w = bs[1], h = relRect.h - bs[1]*2)
            self.image.blit(pygame.transform.smoothscale(textures.gui.R[0],relRect.size),rect)
            
            rect = textures.gui.B[0].get_rect(bottom = relRect.bottom,left = relRect.left+bs[1],w = relRect.w-bs[1]*2,h = bs[1])
            self.image.blit(pygame.transform.smoothscale(textures.gui.B[0],rect.size),rect)
            
            rect = textures.gui.L[0].get_rect(top = relRect.top+bs[1],left = relRect.left,w = bs[1],h = relRect.h - bs[1]*2)
            self.image.blit(pygame.transform.smoothscale(textures.gui.L[0],rect.size),rect)
            
            
            rect = textures.gui.centre[0].get_rect(top = bs[1], left = bs[1], w = relRect.w-bs[1]*2, h = relRect.h - bs[1] * 2)
            self.image.blit(pygame.transform.smoothscale(textures.gui.centre[0],rect.size),rect)
            
        def onClick(self,event):
            print("I was clicked at:",event.pos)
            
    class TextBox(base):
        def __init__(self,parent,relPos = None, absPos = None, text = "", sizeOverride = None):
            self.sizeOverride = sizeOverride
            self.text = text
            baseGUIItems.Button.__init__(self,parent,relPos,absPos)
            if sizeOverride == None:
                self.rect.size = tuple(settings.visuals.font.size(self.text)[x]+textures.gui.buttonSpacing[1]*0.5 for x in range(2))
            else:
                self.rect.size = sizeOverride
            self.genImage()
            self.image.blit(settings.visuals.font.render(self.text, True, (255,255,255)),(textures.gui.buttonSpacing[1]*0.25,textures.gui.buttonSpacing[1]*0.25))
        def genRect(self):
            if self.relative:
                self.rect = self.image.get_rect(topleft = tuple(self.pos[x] + self.parent.rect.topleft[x] for x in range(2)))
            else:
                self.rect = self.image.get_rect(topleft = self.pos)
            
            if self.sizeOverride == None:
                self.rect.size = tuple(settings.visuals.font.size(self.text)[x]+textures.gui.buttonSpacing[1]*0.5 for x in range(2))
            else:
                self.rect.size = self.sizeOverride
                
        def genImage(self):
            self.image = pygame.Surface((self.rect.size),pygame.SRCALPHA,32)
            self.image.fill((0,0,0,127))
            try:
                self.image.blit(settings.visuals.font.render(self.text, True, (255,255,255)),(textures.gui.buttonSpacing[1]*0.25,textures.gui.buttonSpacing[1]*0.25))
            except: 
                pass
class GUIItems():
    class textButton(baseGUIItems.Button):
        def __init__(self,parent,relPos = None, absPos = None, text = "", sizeOverride = None):
            baseGUIItems.Button.__init__(self,parent,relPos,absPos)
            self.text = text
            if sizeOverride == None:
                self.rect.size = tuple(settings.visuals.font.size(text)[x]+textures.gui.buttonSpacing[1]*2.5 for x in range(2))
            else:
                self.rect.size = sizeOverride
            self.genImage()
            self.image.blit(settings.visuals.font.render(text, True, (0,0,0)),(textures.gui.buttonSpacing[1]*1.25,textures.gui.buttonSpacing[1]*1.25))
        def setTarget(self,target,*args,**kwargs):
            self.target = [target,args,kwargs]
        
        def onClick(self,event):
            try:
                x = self.target
                return x[0](*x[1],**x[2])
            except AttributeError: pass
        
            
class debug(pygame.sprite.Group):

    def __init__(self,parent=None):
        pygame.sprite.Group.__init__(self)
        self.parent = parent
        self.rect = pygame.Rect(0,0,250,400)
        self.rect.topright = parent.rect.topright
        self.rect.h = parent.rect.h
        self.makeButtons(self.parent.parent[level.playerLayer].userPlayer)
    
    def makeButtons(self,player):
        if True: #Bombs
            y = baseGUIItems.TextBox(self, relPos = (15,15), text = "Bombs:")
            
            x = GUIItems.textButton(self, absPos = (y.rect.right + 5,15), text = "Increase")
            x.rect.centery = y.rect.centery 
            x.setTarget(entities.player.collect, player, entities.powerups.bombup(dummy = True))
            
            x = GUIItems.textButton(self, absPos = (x.rect.right + 5,15), text = "Decrease")
            x.rect.centery = y.rect.centery
            x.setTarget(entities.player.collect, player, entities.powerups.bombdown(dummy = True))
        
        if True: #Speed
            y = baseGUIItems.TextBox(self, relPos = (15,60), text = "Speed:")
            
            x = GUIItems.textButton(self, absPos = (y.rect.right + 10,15), text = "Increase")
            x.rect.centery = y.rect.centery 
            x.setTarget(entities.player.collect, player, entities.powerups.speedup(dummy = True))
            
            x = GUIItems.textButton(self, absPos = (x.rect.right + 5,15), text = "Decrease")
            x.rect.centery = y.rect.centery
            x.setTarget(entities.player.collect, player, entities.powerups.speeddown(dummy = True))

        if True: #Power
            y = baseGUIItems.TextBox(self, relPos = (15,105), text = "Power:")
            
            x = GUIItems.textButton(self, absPos = (y.rect.right + 10,15), text = "Increase")
            x.rect.centery = y.rect.centery 
            x.setTarget(entities.player.collect, player, entities.powerups.powerup(dummy = True))
            
            x = GUIItems.textButton(self, absPos = (x.rect.right + 5,15), text = "Decrease")
            x.rect.centery = y.rect.centery
            x.setTarget(entities.player.collect, player, entities.powerups.powerdown(dummy = True))
            
        if True: #Piercing
            y = baseGUIItems.TextBox(self, relPos = (15,150), text = "Piercing:")
            
            x = GUIItems.textButton(self, absPos = (y.rect.right + 10,15), text = "On")
            x.rect.centery = y.rect.centery 
            x.setTarget(entities.player.collect, player, entities.powerups.piercing(dummy = True))
            
            x = GUIItems.textButton(self, absPos = (x.rect.right + 10,15), text = "Off")
            x.rect.centery = y.rect.centery 
            x.setTarget(entities.player.collect, player, entities.powerups.piercingoff(dummy = True))
        
        if True: #Kick
            y = baseGUIItems.TextBox(self, relPos = (15,195), text = "Kick:")
            
            x = GUIItems.textButton(self, absPos = (y.rect.right + 10,15), text = "On")
            x.rect.centery = y.rect.centery 
            x.setTarget(entities.player.collect, player, entities.powerups.kick(dummy = True))
            
            x = GUIItems.textButton(self, absPos = (x.rect.right + 10,15), text = "Off")
            x.rect.centery = y.rect.centery 
            x.setTarget(entities.player.collect, player, entities.powerups.kickoff(dummy = True))
class playerStats(pygame.sprite.Group):
    def __init__(self,parent = None):
        pygame.sprite.Group.__init__(self)
        self.parent = parent
        self.player = self.parent.parent[level.playerLayer].userPlayer
        self.rect = pygame.Rect(0,0,0,0)
        self.rect.height = 20*6-1
        self.rect.width  = 100
        self.rect.bottomleft = self.parent.rect.bottomleft
        print(self.rect)
        
        #makeLayout
        self.trackers = {}
        self.trackers["piercing"] = baseGUIItems.TextBox(parent = self, relPos = (5,0), text = "Hello There!")
        self.trackers["kick"] = baseGUIItems.TextBox(parent = self, absPos = (5,self.trackers["piercing"].rect.bottom))
        self.trackers["power"] = baseGUIItems.TextBox(parent = self, absPos = (5,self.trackers["kick"].rect.bottom))
        self.trackers["bombs"] = baseGUIItems.TextBox(parent = self, absPos = (5,self.trackers["power"].rect.bottom))
        self.trackers["bombsRemaining"] = baseGUIItems.TextBox(parent = self, absPos = (5,self.trackers["bombs"].rect.bottom))
        self.trackers["speed"] = baseGUIItems.TextBox(parent = self, absPos = (5,self.trackers["bombsRemaining"].rect.bottom))
        print(self.trackers["piercing"].rect,self.trackers["piercing"])
        self.parent.add(list(self.trackers.values()))

    def update(self):
        self.trackers["piercing"].text = "Piercing: "+str(self.player.powerups.piercing)
        self.trackers["piercing"].genRect()
        self.trackers["piercing"].genImage()
        
        self.trackers["kick"].text = "Kick: "+str(self.player.powerups.kick)
        self.trackers["kick"].genRect()
        self.trackers["kick"].genImage()
        
        self.trackers["power"].text = "Power: "+str(self.player.powerups.power)
        self.trackers["power"].genRect()
        self.trackers["power"].genImage()
        
        self.trackers["bombs"].text = "Bombs: "+str(self.player.powerups.bombs)
        self.trackers["bombs"].genRect()
        self.trackers["bombs"].genImage()
        
        self.trackers["bombsRemaining"].text = "Bombs Remaining: "+str(self.player.powerups.bombsRemaining)
        self.trackers["bombsRemaining"].genRect()
        self.trackers["bombsRemaining"].genImage()
        
        self.trackers["speed"].text = "Speed: "+str(self.player.powerups.speed)
        self.trackers["speed"].genRect()
        self.trackers["speed"].genImage()
        
        
        
        
        
        