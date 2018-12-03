import pygame
import main
import random
import math
from player import Player
from enemy import Enemy
from gameover import Gameover
from numpy import linalg as LA


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE =  (0, 0, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)


class gridLock(main.PygameGame):
    def __init__(self, rootNode, playerSpeed, enemySpeed, enemyNum, width=600, \
            height=400,fps=50,title="GridLock"):
        super().__init__(width, height, fps, title)
        self.rootNode = rootNode
        self.playerSpeed = playerSpeed
        self.enemySpeed = enemySpeed
        self.enemyNum = enemyNum 

    def init(self):
        """
        self.rootNode = 20
        self.playerSpeed = 10
        self.enemySpeed = 4
        self.enemyNum = 10
        """
        self.dict = self.pointDict(self.rootNode)
        self.grid = self.gridMaker(self.rootNode)
        self.player = Player(self.rootNode, self.grid, self.dict, BLUE)
        self.scrollX = -self.dict[self.player.getStart()][0] + self.width // 2
        self.scrollY = -self.dict[self.player.getStart()][1] + self.height // 2
        self.start = self.dict[self.player.getStart()]
        self.enemies = []
        self.timerCount = 0
        
    # grid generation
    @staticmethod
    def gridMaker(rootNode):
        grid = [[] for i in range(pow(rootNode, 2))]
        # create connections for inner points
        for i in range(len(grid)):
            if i // rootNode == (i - 1) // rootNode:
                grid[i].append(i - 1)
            else:
                grid[i].append(None)
            if (i + rootNode) // rootNode < rootNode:
                grid[i].append(i + rootNode)
            else:
                grid[i].append(None)
            if i // rootNode == (i + 1) // rootNode:
                grid[i].append(i + 1)
            else: 
                grid[i].append(None)
            if (i - rootNode) // rootNode >= 0:
                grid[i].append(i - rootNode)
            else:
                grid[i].append(None)
        """ 
        # create diagnoal connections
        for index in range(len(grid)):
            if index % rootNode != rootNode - 1 and index % rootNode \
                    != 0 and index // rootNode < rootNode - 1:
                value = random.randint(-1,1)
                if value == -1: 
                    grid[index].append(index + rootNode - 1)
                    grid[index + rootNode - 1].append(index)
                if value == 1:
                    grid[index].append(index + rootNode + 1)
                    grid[index + rootNode + 1].append(index)
        """
        return grid 

    # maps each index in grid to point through dictionary
    @staticmethod
    def pointDict(rootNode):
        pointDict = {}
        for i in range(pow(rootNode,2)):
            x = 500 * (i % rootNode)
            y = 500 * (i // rootNode)
            xCoord = random.randint(x + 50, x + 450)
            yCoord = random.randint(y + 50, y + 450)
            pointDict[i] = pointDict.get(i, (xCoord, yCoord))
        return pointDict

    # draws nodes
    def drawNode(self, screen, point):
        point = (int(point[0] + self.scrollX), int(point[1] + self.scrollY))
        pygame.draw.circle(screen, BLUE, point, 60)

    # draws edges
    def makeEdge(self, screen, node1, node2):
        node1 = (int(node1[0] + self.scrollX), int(node1[1] + self.scrollY))
        node2 = (int(node2[0] + self.scrollX), int(node2[1] + self.scrollY))
        pygame.draw.line(screen, BLUE, node1, node2, 20)

    # finds slope between two points
    @staticmethod
    def findSlope(p1, p2):
        slope = (p2[1] - p1[1]) / (p2[0] - p1[0])
        norm = LA.norm((1,slope))
        return (1 / norm, slope / norm)

    def mousepressed(self, x, y):
        print(self.message)

    def keyPressed(self, key, mod):
        currPoint = self.player.getEnd()
        if key == pygame.K_LEFT:
            if self.grid[currPoint][0] != None:
                self.nextPoint = self.grid[currPoint][0]
        if key == pygame.K_DOWN:
            if self.grid[currPoint][1] != None:
                self.nextPoint = self.grid[currPoint][1]
        if key == pygame.K_RIGHT:
            if self.grid[currPoint][2] != None:
                self.nextPoint = self.grid[currPoint][2]
        if key == pygame.K_UP:
            if self.grid[currPoint][3] != None:
                self.nextPoint = self.grid[currPoint][3]
        self.player.queuePoint(self.nextPoint)

    def playerMove(self):
        start = self.start
        end = self.dict[self.player.getEnd()]
        speed = self.playerSpeed
        if not math.isclose(start[0], end[0], abs_tol = speed) \
                or not math.isclose(start[1], end[1], abs_tol = speed):
            slope = self.findSlope(start, end)
            if end[0] > start[0]:
                start = (start[0] + speed * slope[0], start[1] + speed * slope[1])
                self.scrollX -= speed * slope[0]
                self.scrollY -= speed * slope[1]
            else:
                start = (start[0] - speed * slope[0], start[1] - speed * slope[1])
                self.scrollX += speed * slope[0]
                self.scrollY += speed * slope[1]
            self.start = start
        else:
            self.player.nextMove()
            self.scrollX = -self.dict[self.player.getStart()][0] + self.width // 2
            self.scrollY = -self.dict[self.player.getStart()][1] + self.height // 2
            self.start = self.dict[self.player.getStart()]

    def enemyMove(self, enemy):
        start = enemy.currPos 
        end = self.dict[enemy.getEnd()]
        speed = self.enemySpeed
        if not math.isclose(start[0], end[0], abs_tol = speed) \
                or not math.isclose(start[1], end[1], abs_tol = speed):
            slope = self.findSlope(start, end)
            if end[0] > start[0]:
                start = (start[0] + speed * slope[0], start[1] + speed * slope[1])
            else:
                start = (start[0] - speed * slope[0], start[1] - speed * slope[1])
            enemy.currPos = start
        else:
            enemy.nextMove()
            enemy.optimalPath(self.player)

    def timerFired(self, dt):
        if self.timerCount % 120 == 0 and len(self.enemies) < self.enemyNum:
            self.enemies.append(Enemy(self.rootNode, self.grid, self.dict, RED))
        for enemy in self.enemies:
            self.enemyMove(enemy)
        self.playerMove() 
        self.timerCount += 1


    def redrawAll(self, screen):
        for i in range(len(self.grid)):
            for j in self.grid[i]:
                if j == None:
                    continue
                else:
                    self.makeEdge(screen, self.dict[i], self.dict[j])

        for point in self.dict.values():
            self.drawNode(screen, point)
        
        for enemy in self.enemies:
            pygame.draw.circle(screen, RED, (int(enemy.currPos[0] + self.scrollX), int(enemy.currPos[1] + self.scrollY)), 50)
            if math.isclose(enemy.currPos[0] + self.scrollX, self.width // 2, abs_tol = 10) \
                    and math.isclose(enemy.currPos[1] + self.scrollY, self.height // 2, abs_tol = 10):
                pass
                #gameover = Gameover()
                #gameover.run()

        pygame.draw.circle(screen, BLACK, (self.width // 2, self.height//2), 50)
       
#creating and running the game
"""
def __init__(self, rootNode, playerSpeed, enemySpeed, enemyNum, width=600, \
            height=400,fps=50,title="GridLock")
"""
game = gridLock(7, 8, 6, 5, 3000, 1200, 150)
game.run()
