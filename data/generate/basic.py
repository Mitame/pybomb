class grid():
    
    def __init__(self,size,fill=None):
        self._map = []
        self.size = size
        for y in range(size[1]):
            m = []
            for x in range(size[0]):
                if fill is not None:
                    m.append(fill)
                else:
                    m.append((x+1,y+1))
            self._map.extend(m)
    def set(self,position,data,kill = True):
        i = self._conv(p=position)
        if i is not False:
            if kill:
                try:
                    self._map[i].kill()
                except:
                    pass
            self._map[i] = data
    
    def get(self,position):
        try:
            return self._map[self._conv(p=position)]
        except:
            return False
        
    def find(self,item):
        if item in self._map:
            return self._conv(i=self._map.index(item))
        else:
            return False
        
    def move(self,fromPos,toPos,swap=False,killNew = True):
        if self.within(fromPos) and self.within(toPos):
            item = self.get(fromPos)
            if swap:
                self.set(fromPos,self.get(toPos),kill=False)
            else:
                self.set(fromPos,0,kill=False)
            self.set(toPos,item,killNew)
        else:
            return False
    
    def dupe(self,fromPos,toPos):
        if self.within(fromPos) and self.within(toPos):
            self.set(self.get(fromPos),toPos)
        else:
            return False
    def within(self,pos):
        return ((self.size[0] > pos[0] >= 0) and (self.size[1] > pos[1] >= 0))
    
    def __str__(self):
        return "\n".join(str(self._map[self.size[0]*y:self.size[0]*(y+1)]) for y in range(self.size[1]))
    
    def __iter__(self):
        return (x for x in self._map)
    
    def __getitem__(self,x):
        return self._map[x]
        
    def _conv(self,p=None,i=None):
        if p is not None:
            p = list(p)
            if self.within(p):
                i = self.size[0]*p[1]+p[0]
                return i
            else:
                return False
        elif i is not None:
            return i%self.size[0],i//self.size[0]
            
def tests():
    test = grid((10,5))
    print(test)
    print(test.find((6,5)))
    print(test.get((3,4)))

if __name__ == "__main__": tests()