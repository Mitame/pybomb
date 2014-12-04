import data

def nuke(entLayer):
    spawnTick = data.timing.queue.tick
    for x in range(data.settings.mapSize[0]):
        for y in range(data.settings.mapSize[1]):
            entLayer.grid.set((x,y),data.entities.blast(entLayer, spawnTick, False, data.entities.world))
#             entLayer.grid.set((x,y),data.entities.bomb(entLayer, placer = data.entities.world, spawntick = spawnTick))
            entLayer.grid.get((x,y)).genRect()

def maxPower(player):
    player.powerups.speed = data.bases.Powerups.maxSpeed
    player.powerups.power = data.bases.Powerups.maxPower
    player.powerups.bombs = data.bases.Powerups.maxBombs
    player.powerups.piercing = True
    player.powerups.kick = True
    
    