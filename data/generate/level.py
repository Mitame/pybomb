import data.block as block
import data.settings as settings



def generate(parent,LevelType):
    global basic
    import data.generate.basic as basic
    result = levelTypes[LevelType](parent)
    for blk in parent.grid._map:
        blk.update(True,True)
    return result

def classic(parent):
    
    parent.grid = basic.grid(settings.mapSize,0)
        
    #Fill with empty or breakable blocks
    for pos in ((x,y) for x in range(parent.grid.size[0]) for y in range(parent.grid.size[1])):
        parent.grid.set(pos,block.emptyOrBreakable(parent),False)
    
    
    #add solid blocks
    for pos in ((x,y) for x in range(1,parent.grid.size[0],2) for y in range(1,parent.grid.size[1],2)):
        parent.grid.set(pos,block.unbreakable(parent),True)
    
    #clear spawn areas
    
    for spawn in parent.spawnAreas:
        parent.grid.set(spawn,block.spawn(parent))
        for offset in ((1,0),(0,1),(-1,0),(0,-1)):
            pos = tuple(spawn[a]+offset[a] for a in range(2))
            if parent.grid.within(pos):
                if type(parent.grid.get(pos)) == block.breakable:
                    parent.grid.set(pos, block.empty(parent))
                
        
def empty(parent):
    parent.grid = basic.grid(settings.mapSize,0)
        
    #Fill with empty or breakable blocks
    for pos in ((x,y) for x in range(parent.grid.size[0]) for y in range(parent.grid.size[1])):
        parent.grid.set(pos,block.empty(parent),False)
    
    #add solid blocks
    for pos in ((x,y) for x in range(1,parent.grid.size[0],2) for y in range(1,parent.grid.size[1],2)):
        parent.grid.set(pos,block.unbreakable(parent),True)
    

def wasteland(parent):
    parent.grid = basic.grid(settings.mapSize,0)
        
    #Fill with empty or breakable blocks
    for pos in ((x,y) for x in range(parent.grid.size[0]) for y in range(parent.grid.size[1])):
        parent.grid.set(pos,block.empty(parent),False)
    

def destructionDerby(parent):
    parent.grid = basic.grid(settings.mapSize,0)
        
    #Fill with empty or breakable blocks
    for pos in ((x,y) for x in range(parent.grid.size[0]) for y in range(parent.grid.size[1])):
        parent.grid.set(pos,block.breakable(parent),False)
    
    #clear spawn areas    
    for spawn in parent.spawnAreas:
        parent.grid.set(spawn,block.spawn(parent))
        for offset in ((1,0),(0,1),(-1,0),(0,-1)):
            pos = tuple(spawn[a]+offset[a] for a in range(2))
            if parent.grid.within(pos):
                if type(parent.grid.get(pos)) == block.breakable:
                    parent.grid.set(pos, block.empty(parent))
    
    #generate sprite rects

def conveyors(parent):
    pass
    wasteland(parent)
    for x in range(settings.mapSize[0]-2):
        x += 1
        parent.grid.set((x,1),block.conveyor(parent,"R"))
        parent.grid.set((x,settings.mapSize[1]-2),block.conveyor(parent,"R"))
    
levelTypes = [classic,empty,wasteland,destructionDerby,conveyors]