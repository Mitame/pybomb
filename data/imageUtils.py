import pygame.transform,pygame.image,pygame.surface,pygame.rect
import data.settings as settings

def crop(surf,area,transparent = True, size = settings.gridSize):
    area = pygame.Rect(area)
    if transparent:
        result = pygame.surface.Surface(area.size, pygame.SRCALPHA,32)
    else:
        result = pygame.surface.Surface(area.size)
    result.blit(surf,(0,0),area)
    result.set_colorkey(settings.alphaColour)
    if size:
        return resize(result,size)
    else:
        return result

def resize(surf,size):
    size = tuple(int(size[x]) for x in range(2))
    if settings.smoothscale and size[0] < surf.get_size()[0]:
        return pygame.transform.smoothscale(surf, size)
    else:
        
        return pygame.transform.scale(surf, size)