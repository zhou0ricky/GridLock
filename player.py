import random

class Player(object):
    def __init__(self, rootNode, grid, dictionary, color):
        self.rootNode = rootNode
        self.start = random.randint(0, len(grid) - 1)        
        if grid[self.start][1] == None:
            self.end = grid[self.start][3]
        else:
            self.end = grid[self.start][1]
        self.color = color 
        self.queue = self.end
        self.dictionary = dictionary
        self.currPos = dictionary[self.start]

    def getStart(self):
        return self.start
    
    def queuePoint(self, point):
        self.queue = point

    def nextMove(self):
        self.start = self.end
        self.end = self.queue
        
    def getEnd(self):
        return self.end
    


