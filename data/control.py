import pygame.event
import time
from data import *
import data
# import data.settings as settings
import data.entities as entities
import data.gui as gui
# from settings import level 
# import data.timing as timing
# import data.level as level
bgColour = pygame.Color(0,0,0)
def eventLoop():
    while 1:
        pygame.event.pump()
        if pygame.event.peek(pygame.QUIT):
            break
        pygame.event.clear()
        time.sleep(1/30)
    settings.close()

def loadMenu(menu):
    if menu:
        pass
def clickBomb(groupContainer,screen=None):
    if screen == None:
        screen = pygame.display.set_mode(tuple(groupContainer[level.Map].grid.size[x]*groupContainer[level.Map].gridSize[x] for x in range(2)))
    while 1:
        pygame.event.pump()
        if pygame.event.peek(pygame.QUIT):
            break
        for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            gridpos = tuple(event.pos[x]//settings.gridSize[x] for x in range(2))
            groupContainer[level.entLayer].grid.set(gridpos,entities.bomb(groupContainer[level.entLayer]))
            groupContainer[level.entLayer].grid._map[groupContainer[level.entLayer].grid._conv(p=(gridpos))].genRect()
            print("Bomb placed at",gridpos)
        pygame.event.clear()
        screen.fill(bgColour)
        groupContainer[level.Map].draw(screen)
        groupContainer[level.entLayer].draw(screen)
        pygame.display.flip()
        time.sleep(1/30)
    settings.close()
def extraControl(groupContainer,event=None,key = None,action = None):
    if event:
        action = settings.controls.player[event.key]
    elif key:
        action = settings.controls.player[key]
    elif action == None:
        return
    
    if action == "toggleHUD":
        groupContainer[level.GUI].toggleLayout(gui.playerStats,"mainPlayerStats")
    
    elif action == "quit":
        settings.close()
    

def withPlayers(groupContainer,screen=None):
    if screen == None:
        try:
            screen = pygame.display.set_mode(settings.screensize)
        except:
            size = tuple(groupContainer[level.Map].grid.size[x]*groupContainer[level.Map].gridSize[x] for x in range(2))
            if texture.bgPadding:
                size = tuple(size[x]+texture.bgPadding[x]*2 for x in range (2))
            print("Settings screen to size'",size,"'.")
            screen = pygame.display.set_mode(size)
    cheatContainer = bases.cheats()
    cheatContainer.addCheat("poiop", "Debug", groupContainer[level.GUI].toggleLayout, gui.debug, "Debug Menu")
    cheatContainer.addCheat("killmenow", "Commit Suicide", groupContainer[level.playerLayer].userPlayer.kill)
    cheatContainer.addCheat("itsalive", "Respawn", groupContainer[level.playerLayer].userPlayer.action, action="respawn")
    cheatContainer.addCheat("canttouchthis", "Invulnerability", groupContainer[level.playerLayer].userPlayer.collect, entities.powerups.invulnerable(dummy=True))
    cheatContainer.addCheat("settheworldonfire","Nuke!!!", data.cheats.nuke, groupContainer[level.entLayer])
    cheatContainer.addCheat("over9000","Full PowerUPS",data.cheats.maxPower,groupContainer[level.playerLayer].userPlayer)
    
    level.GUI.rect = screen.get_rect()
    
    heldKeys = []
    groupContainer[level.GUI].toggleLayout(gui.playerStats,"mainPlayerStats")
    while 1:
        start = time.time()
        pygame.event.pump()
        if pygame.event.peek(pygame.QUIT):
            break
        
        for event in pygame.event.get(pygame.KEYDOWN):
            cheatContainer.keypresses += event.unicode
            
        for key in settings.controls.player.keys():
            if pygame.key.get_pressed()[key]:
                if not groupContainer[level.playerLayer].userPlayer.moving:
                    groupContainer[level.playerLayer].userPlayer.action(key=key)
                
        if pygame.event.peek(pygame.MOUSEMOTION) or pygame.event.peek(pygame.MOUSEBUTTONDOWN):
            groupContainer[level.GUI].manageClicks()
        pygame.event.clear()
        
        cheatContainer.update(True, groupContainer[level.GUI])
#         screen.fill(bgColour)
        screen.blit(texture.bg,(0,0))
        
        groupContainer[level.Map].draw(screen)
         
        groupContainer[level.entLayer].runOnSprites(entities.bomb.update,sprType = entities.bomb)
        groupContainer[level.entLayer].draw(screen)
         
        groupContainer[level.playerLayer].update()
        groupContainer[level.playerLayer].draw(screen)
        
        groupContainer[level.extraMap].update() 
        groupContainer[level.extraMap].draw(screen)
        
        if "mainPlayerStats" in groupContainer[level.GUI].layouts.keys():
            groupContainer[level.GUI].layouts["mainPlayerStats"].update()
        groupContainer[level.GUI].draw(screen)
        
        pygame.display.flip()
        wait = 1/settings.tickPerSec-time.time()+start
        if wait > 0:
                time.sleep(wait)
        else:
            print("Render Slow,",-wait,"s missed")
    settings.close()
    