import random
from player import Player

class Enemy(Player):
    def optimalPath(self, player):
        start = self.start
        goal = player.getEnd()
        horiz = (goal % self.rootNode) - (start % self.rootNode)
        vert = (goal // self.rootNode) - (start // self.rootNode)
        if horiz == 0 and vert == 0:
            self.end = player.getStart()
        elif horiz == 0:
            if vert > 0:
                self.end = self.start + self.rootNode
            elif vert < 0:
                self.end = self.start - self.rootNode
            else: 
                pass
        elif vert == 0:
            if horiz > 0:
                self.end = self.start + 1
            elif horiz < 0:
                self.end = self.start - 1
            else: 
                pass
        else:
            choose = random.randint(0,1)
            if choose == 0:
                if vert > 0:
                    self.end = self.start + self.rootNode
                elif vert < 0:
                    self.end = self.start - self.rootNode
                else: 
                    pass
            elif choose == 1:
                if horiz > 0:
                    self.end = self.start + 1
                elif horiz < 0:
                    self.end = self.start - 1
                else: 
                    pass

    def nextMove(self):
        self.start = self.end
        self.currPos = self.dictionary[self.start]

    def setcurrPos(self, point):
        self.currPos = point


