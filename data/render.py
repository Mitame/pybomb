import pygame
import time
# import data.settings as settings
import data.control
def staticSprite(sprite):
    screen = pygame.display.set_mode((sprite.rect.size))
    screen.blit(sprite.image,(0,0))
    pygame.display.flip()
    data.control.eventLoop()

def staticGroup(group):
    surf = pygame.Surface((800,800))
    surf.fill((255,255,255))
    group.draw(surf)
    print(group)
    screen = pygame.display.set_mode(surf.get_size())
    screen.blit(surf,(0,0))
    pygame.display.flip()
    data.control.eventLoop()

def staticLevel(level):
    surf = pygame.Surface(tuple(level.grid.size[x]*level.gridSize[x] for x in range(2)))
    screen = pygame.display.set_mode(surf.get_size())
    level.draw(screen)
    pygame.display.flip()
    data.control.eventLoop()

def staticLevelandEnts(level,eventRead=data.control.eventLoop,*other):  
    screen = pygame.display.set_mode(tuple(level.grid.size[x]*level.gridSize[x] for x in range(2)))
    eventRead(screen,level,other[0])