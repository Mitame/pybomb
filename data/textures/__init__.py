import pygame
import data.imageUtils as imageUtils
import data.settings as settings

textureSize = (64,64)
extraOnBlocks = True
bgPadding = list(int((32,128,32,8)[x]*(settings.gridSize[x]/textureSize[x])) for x in range(2))
bgPadding.extend((8,20))
print(bgPadding)

def poscalc(pos,sep = None):
    if sep:
        return tuple(sep[x]*pos[x] for x in range(2))
    else:
        return tuple(textureSize[x]*pos[x] for x in range(2))

def extraPosCalc(pos):
    return (tuple(poscalc(pos)[x]+(0,textureSize[1]*0.75)[x] for x in range(2)),tuple(textureSize[x]*(1,0.25)[x] for x in range(2)))

def reverse(iterable):
    temp = [None]
    for x in iterable:
        temp.insert(0,x)
    temp.pop()
    return temp
class rawTextures():
    terrain = pygame.image.load(r"./data/textures/terrain2.png")
    entities = pygame.image.load(r"./data/textures/entities.png")
    blasts = pygame.image.load(r"./data/textures/blasts.png")
    player = pygame.image.load(r"./data/textures/player3.png")
    playerTrans = pygame.image.load(r"./data/textures/playerTrans.png")
    gui = pygame.image.load(r"./data/textures/gui.png")
    bg = pygame.image.load(r"./data/textures/bgComponents.png")

bg = pygame.Surface(settings.screensize)

def makeBG():
    mul = 2
    topBrickPlacement = pygame.Rect(0,0,24*mul,20*mul)
    frontBrickPlacement = pygame.Rect(0,20*mul,16*mul,12*mul)
    sideBrickPlacement = pygame.Rect(0,32*mul,14*mul,24*mul)
    
    topBrick = imageUtils.crop(rawTextures.bg,topBrickPlacement,size = False)
    frontBrick = imageUtils.crop(rawTextures.bg,frontBrickPlacement,size = False)
    sideBrick = imageUtils.crop(rawTextures.bg,sideBrickPlacement,size = False)
    
    ymul = 0
    while 1:
        bg.blit(sideBrick, sideBrick.get_rect(top = sideBrick.get_height()*ymul, right = bgPadding[0]))
        bg.blit(sideBrick, sideBrick.get_rect(top = sideBrick.get_height()*ymul, left = settings.screensize[0]-bgPadding[0]))
        ymul += 1
        if ymul*topBrick.get_height() > settings.screensize[1]:
            break
    
    xmul = 0
    while 1:
        bg.blit(topBrick, topBrick.get_rect(top = 0, left = bgPadding[0]+topBrick.get_width()*xmul))
        bg.blit(topBrick, topBrick.get_rect(bottom = settings.screensize[1], left = bgPadding[0]+topBrick.get_width()*xmul))
        xmul += 1
        if (xmul+1)*topBrick.get_width() > settings.screensize[0]-bgPadding[0]*2:
            break
    
    xmul = 0
    while 1:
        bg.blit(frontBrick, frontBrick.get_rect(top = topBrick.get_height(), left = bgPadding[0]+frontBrick.get_width()*xmul))
        xmul += 1
        if (xmul+1)*frontBrick.get_width() > settings.screensize[0]-bgPadding[0]*2:
            break

class block():
    empty0 = imageUtils.crop(rawTextures.terrain,(poscalc((0,0)),textureSize))
    empty1 = imageUtils.crop(rawTextures.terrain,(poscalc((0,1)),textureSize))
    empty2 = imageUtils.crop(rawTextures.terrain,(poscalc((0,2)),textureSize))
    empty3 = imageUtils.crop(rawTextures.terrain,(poscalc((0,3)),textureSize))
    empty4 = imageUtils.crop(rawTextures.terrain,(poscalc((0,4)),textureSize))
    breakable = imageUtils.crop(rawTextures.terrain,(poscalc((2,1)),textureSize))
    unbreakable = imageUtils.crop(rawTextures.terrain,(poscalc((3,1)),textureSize))
    if extraOnBlocks:
        class extra():
            breakable = imageUtils.crop(rawTextures.terrain,extraPosCalc((2,0)),size = tuple(settings.gridSize[x]*(1,0.25)[x] for x in range(2)))
            unbreakable = imageUtils.crop(rawTextures.terrain,extraPosCalc((3,0)),size = tuple(settings.gridSize[x]*(1,0.25)[x] for x in range(2)))
    
class entities():
    bomb0 = imageUtils.crop(rawTextures.entities,(poscalc((0,0)),textureSize))
    bomb1 = imageUtils.crop(rawTextures.entities,(poscalc((0,1)),textureSize))
    
    speedup = imageUtils.crop(rawTextures.entities,(poscalc((1,0)),textureSize))
    bombup = imageUtils.crop(rawTextures.entities,(poscalc((2,0)),textureSize))
    powerup = imageUtils.crop(rawTextures.entities,(poscalc((3,0)),textureSize))
    piercing = imageUtils.crop(rawTextures.entities,(poscalc((5,0)),textureSize))
    kick = imageUtils.crop(rawTextures.entities,(poscalc((4,0)),textureSize))
    
    speeddown = imageUtils.crop(rawTextures.entities,(poscalc((1,1)),textureSize))
    bombdown = imageUtils.crop(rawTextures.entities,(poscalc((2,1)),textureSize))
    powerdown = imageUtils.crop(rawTextures.entities,(poscalc((3,1)),textureSize))
    piercingoff = imageUtils.crop(rawTextures.entities,(poscalc((5,1)),textureSize))
    kickoff = imageUtils.crop(rawTextures.entities,(poscalc((4,1)),textureSize))

class blast():
    animLength = 4
    R = []
    D = []
    L = []
    U = []
    
    RL = []
    DU = []
    
    RU = []
    RD = []
    DL = []
    LU = []
    
    RLU = []
    RDU = []
    RDL = []
    DLU = []
    
    ALL = []

#fill blast lists

def loadBlast():
    for x in range(0,blast.animLength):
        blast.R.append(imageUtils.crop(rawTextures.blasts,(poscalc((11,x)),textureSize)))
        blast.D.append(imageUtils.crop(rawTextures.blasts,(poscalc((12,x)),textureSize)))
        blast.L.append(imageUtils.crop(rawTextures.blasts,(poscalc((13,x)),textureSize)))
        blast.U.append(imageUtils.crop(rawTextures.blasts,(poscalc((14,x)),textureSize)))
    
        blast.RL.append(imageUtils.crop(rawTextures.blasts,(poscalc((0,x)),textureSize)))
        blast.DU.append(imageUtils.crop(rawTextures.blasts,(poscalc((1,x)),textureSize)))
    
        blast.RU.append(imageUtils.crop(rawTextures.blasts,(poscalc((2,x)),textureSize)))
        blast.RD.append(imageUtils.crop(rawTextures.blasts,(poscalc((3,x)),textureSize)))
        blast.DL.append(imageUtils.crop(rawTextures.blasts,(poscalc((4,x)),textureSize)))
        blast.LU.append(imageUtils.crop(rawTextures.blasts,(poscalc((5,x)),textureSize)))
    
        blast.RLU.append(imageUtils.crop(rawTextures.blasts,(poscalc((6,x)),textureSize)))
        blast.RDU.append(imageUtils.crop(rawTextures.blasts,(poscalc((7,x)),textureSize)))
        blast.RDL.append(imageUtils.crop(rawTextures.blasts,(poscalc((8,x)),textureSize)))
        blast.DLU.append(imageUtils.crop(rawTextures.blasts,(poscalc((9,x)),textureSize)))
    
        blast.ALL.append(imageUtils.crop(rawTextures.blasts,(poscalc((10,x)),textureSize)))

class player():
    textureSize = (26,38)
    reSize = (32,47)
    additional = (0,0)
    animSpeedMultiplyer = 4
    animLength = 9
    animFrames = 30
    animOrder = (4,5,6,7,8,1,2,3)
    animIdle = 0
    
    
    R = []
    D = []
    L = []
    U = []
    Death = []
    
    class transparent():
        animLength = 3
        animFrames = 3
        R = []
        D = []
        L = []
        U = []

def loadPlayer():
    for y in range(player.animLength):
        player.R.append(imageUtils.crop(rawTextures.player,(poscalc((0,y),player.textureSize),player.textureSize),size = player.reSize))
        player.D.append(imageUtils.crop(rawTextures.player,(poscalc((1,y),player.textureSize),player.textureSize),size = player.reSize))
        player.L.append(imageUtils.crop(rawTextures.player,(poscalc((2,y),player.textureSize),player.textureSize),size = player.reSize))
        player.U.append(imageUtils.crop(rawTextures.player,(poscalc((3,y),player.textureSize),player.textureSize),size = player.reSize))
    
        player.transparent.R.append(imageUtils.crop(rawTextures.playerTrans,(poscalc((0,y),player.textureSize),player.textureSize),size = player.reSize))
        player.transparent.D.append(imageUtils.crop(rawTextures.playerTrans,(poscalc((1,y),player.textureSize),player.textureSize),size = player.reSize))
        player.transparent.L.append(imageUtils.crop(rawTextures.playerTrans,(poscalc((2,y),player.textureSize),player.textureSize),size = player.reSize))
        player.transparent.U.append(imageUtils.crop(rawTextures.playerTrans,(poscalc((3,y),player.textureSize),player.textureSize),size = player.reSize))
        
class gui():
    buttonSpacing = (pygame.Rect(0,0,64,64),8)
    R = []
    B = []
    L = []
    T = []
    
    RB = []
    BL = []
    LT = []
    TR = []
    
    centre = []  
        
def loadGUI():
    bs = gui.buttonSpacing
#     gui.R.append(imageUtils.crop(rawTextures.gui,(bs[0].w-bs[1],0,bs[1],bs[0].h)))
    for i in range(2):
        
        gui.R.append(imageUtils.crop(rawTextures.gui, (bs[0].w*(i+1)-bs[1], bs[1], bs[1], bs[0].h-bs[1]*2), size = None))
        gui.B.append(imageUtils.crop(rawTextures.gui, (bs[0].w*i+bs[1], bs[0].h-bs[1], bs[0].w-bs[1]*2, bs[1]), size = None))
        gui.L.append(imageUtils.crop(rawTextures.gui, (bs[0].w*i, bs[1], bs[1], bs[0].h-bs[1]*2), size = None))
        gui.T.append(imageUtils.crop(rawTextures.gui, (bs[0].w*i+bs[1], 0, bs[0].w-bs[1]*2, bs[1]), size = None))
        
        gui.RB.append(imageUtils.crop(rawTextures.gui, (bs[0].w*(i+1)-bs[1], bs[0].h-bs[1], bs[1],bs[1]), size = None))
        gui.BL.append(imageUtils.crop(rawTextures.gui, (bs[0].w*i, bs[0].h-bs[1], bs[1],bs[1]), size = None))
        gui.LT.append(imageUtils.crop(rawTextures.gui, (bs[0].w*i+bs[1], 0, bs[1],bs[1]), size = None))
        gui.TR.append(imageUtils.crop(rawTextures.gui, (bs[0].w*(i+1)-bs[1], 0, bs[1],bs[1]), size = None))
        
        gui.centre.append(imageUtils.crop(rawTextures.gui, (bs[0].w*i+bs[1], bs[1], bs[0].w-bs[1]*2, bs[0].h-bs[1]*2)))
    
    
loadBlast()
loadPlayer()
loadGUI()
makeBG()

def test():
    import time
    allImgs = []
    allImgs.extend(player.R)
    allImgs.extend(player.D)
    allImgs.extend(player.L)
    allImgs.extend(player.U)
#     for dire in vars(blast).items():
#         if dire[0][:2] != "__":
#             allImgs.extend(dire[1])
    screen = pygame.display.set_mode(settings.gridSize)
    while 1:
        for x in allImgs:
            pygame.event.pump()
            if pygame.event.peek(pygame.QUIT):
                raise SystemExit
            pygame.event.clear()
            
            screen.fill((0,0,0))
            screen.blit(x,(0,0))
            pygame.display.flip()
            time.sleep(0.2)

if __name__ == "__main__": test()
