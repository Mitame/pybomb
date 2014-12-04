'''
Created on 9 May 2014

@author: Levi Wright
'''
import os
if os.getcwd()[-4:] == "data":
    os.chdir("..")
running = True

import data
import pygame

mapSize = (15,19)
gridSize= (32,32)
screensize = (512,710)
tickPerSec = 30
alphaColour = (255,0,255)
smoothscale = True

playerName = "Mr. Mind Implosion"
class gameplay():
    ghosting = True
    ghostMaxDensity = 2 #-1 = can't move, 0 = empty only, 1 = breakable and empty, 2 = unbreakable blocks
    
    deathDropPowerups = True
    deathDropChance = 50
    
    maxPowerup = False
    
    spawnPowerUps = True and not maxPowerup
    spawnPowerDowns = True and not maxPowerup
    spawnViruses = True and not maxPowerup
    
    baseMovementSpeed = 3
    bombSpeed = 1
    
    lockToGrid = True

class networking():
    port = 7777
    ip = "localhost"
    host = True

class levelGen():
    blockEmpty = 3
    spawnAreas = []
    spawnAreaChance = None
    type = 3
    
for mul in ((1,1),(1,0),(0,1),(0,0)):
    levelGen.spawnAreas.append(tuple((mapSize[x]-1)*mul[x] for x in range(2)))

dropChance = None
def genChance():
    global dropChance
    dropChance = data.bases.randomChoice()
    if gameplay.spawnPowerUps:
        dropChance.addChoice(data.entities.powerups.speedup, 20)
        dropChance.addChoice(data.entities.powerups.powerup, 20)
        dropChance.addChoice(data.entities.powerups.bombup, 20)
        dropChance.addChoice(data.entities.powerups.kick, 10)
        dropChance.addChoice(data.entities.powerups.piercing, 5)
    
    if gameplay.spawnPowerDowns:
        dropChance.addChoice(data.entities.powerups.speeddown, 5)
        dropChance.addChoice(data.entities.powerups.powerdown, 5)
        dropChance.addChoice(data.entities.powerups.bombdown, 5)
        dropChance.addChoice(data.entities.powerups.kickoff, 2)
        dropChance.addChoice(data.entities.powerups.piercingoff, 1)
    
    if gameplay.spawnViruses:
        dropChance.addChoice(data.entities.powerups.diarrhea,5)
    dropChance.addChoice(None, 200-dropChance.getTotalChance())
    
    levelGen.spawnAreaChance = data.bases.randomChoice()
    for x in levelGen.spawnAreas:
        levelGen.spawnAreaChance.addChoice(x,1)
#     print(levelGen.spawnAreaChance)

class controls():
    player = {pygame.K_w:"walkUp",
            pygame.K_UP:"walkUp",
              pygame.K_s:"walkDown",
            pygame.K_DOWN:"walkDown",
              pygame.K_a:"walkLeft",
            pygame.K_LEFT:"walkLeft",
              pygame.K_d:"walkRight",
            pygame.K_RIGHT:"walkRight",
              pygame.K_SPACE:"dropBomb",
            pygame.K_RETURN:"dropBomb",
              pygame.K_r:"respawn",
              pygame.K_k:"killSelf"}              

pygame.font.init()
class visuals():
    font = pygame.font.SysFont("Ubuntu", 12)
    hideHUDonDeath = True

def close():
    global running
    running = False
    raise SystemExit

def main():
    genChance()
    data.level.test()
#     data.texture.test()
    
if __name__ == "__main__": main()