from data import level,entities

class NPC(entities.player):
    class control():
        wish = None
        accessableGrids = []
    def update(self):
        entities.player.update(self)

    def getAccessable(self):
        g_get = self.parent.baseLevel.grid.get
    