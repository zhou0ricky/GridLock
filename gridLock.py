import pygame
import main
import random
import math
from player import Player
from enemy import Enemy
from gameover import Gameover
from numpy import linalg as LA
import menu
import os


# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE =  (0, 0, 255)
GREEN = (0, 255, 0)
RED =   (255, 0, 0)

#fonts
font = "StressGenesis.otf"

class gridLock(main.PygameGame):
    def __init__(self, rootNode, playerSpeed, enemySpeed, enemyNum, width=600, \
            height=400,fps=50,title="GridLock"):
        super().__init__(width, height, fps, title)
        self.bgColor = BLACK
        self.rootNode = rootNode
        self.playerSpeed = playerSpeed
        self.enemySpeed = enemySpeed
        self.enemyNum = enemyNum 
        self.score = 0
        self.inner = 25
        self.grow = True

    def setDifficulty(self, mode):
        self.difficulty = mode
        if mode == 0:
            self.enemySpeed = 2
            self.enemyNum = 5
        if mode == 1: 
            self.enemySpeed = 4
            self.enemyNum = 7
        if mode == 2:
            self.enemySpeed = 6
            self.enemyNum = 9

    def init(self):
        self.dict = self.pointDict(self.rootNode)
        self.grid = self.gridMaker(self.rootNode)
        self.player = Player(self.rootNode, self.grid, self.dict, BLUE)
        self.scrollX = -self.dict[self.player.getStart()][0] + self.width // 2
        self.scrollY = -self.dict[self.player.getStart()][1] + self.height // 2
        self.start = self.dict[self.player.getStart()]
        self.scoreList = self.text_format(str(self.score), font, 100, WHITE)
        self.scoreList_rect = self.scoreList.get_rect() 
        self.enemies = []
        self.powerups = []
        self.timerCount = 0
        self.timeFreeze = False
        self.powerupTimer = 0
        self.placeholder = 0
        self.usePowerUp = False
        self.pSpeedInc = False
        self.eSpeedInc = False
        self.pSpeedDec = False
        self.eSpeedDec = False
        
    # Text Renderer
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

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
        pygame.draw.circle(screen, WHITE, point, 60)
        pygame.draw.circle(screen, BLACK, point, 57)

    # draws edges
    def makeEdge(self, screen, node1, node2):
        node1 = (int(node1[0] + self.scrollX), int(node1[1] + self.scrollY))
        node2 = (int(node2[0] + self.scrollX), int(node2[1] + self.scrollY))
        pygame.draw.line(screen, WHITE, node1, node2, 3)

    # finds slope between two points
    @staticmethod
    def findSlope(p1, p2):
        if p2[0] - p1[0] == 0:
            return (0, 1)
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

    def spawnPowerUp(self):
        point = random.randint(0, len(self.dict.values()) - 1)
        powerup = random.randint(0, 4)
        notin = True
        for pair in self.powerups:
            if point == pair[0]:
                self.spawnPowerUp()
                notin = False
        if notin == True:
            self.powerups.append((point, powerup))

    def timeFrozen(self):
        if self.timeFreeze == False:
            self.usePowerUp = True
            self.timeFreeze = True
        else:
            self.usePowerUp = False
            self.timeFreeze = False
    
    def playerSpeedUp(self):
        if self.pSpeedInc == False:
            self.usePowerUp = True
            self.pSpeedInc = True
            self.placeholder = self.playerSpeed
            self.playerSpeed = self.playerSpeed * 1.25
        else:
            self.usePowerUp = False
            self.playerSpeed = self.placeholder
            self.pSpeedInc = False

    def enemySlowDown(self):
        if self.eSpeedDec == False:
            self.usePowerUp = True
            self.eSpeedDec = True
            self.placeholder = self.enemySpeed
            self.enemySpeed = self.enemySpeed * 0.75
        else:
            self.usePowerUp = False
            self.enemySpeed = self.placeholder 
            self.eSpeedDec = False

    def enemySpeedUp(self):
        if self.eSpeedInc == False:
            self.usePowerUp = True
            self.eSpeedInc = True
            self.placeholder = self.enemySpeed
            self.enemySpeed = self.enemySpeed * 1.25
        else: 
            self.usePowerUp = False
            self.enemySpeed = self.placeholder
            self.eSpeedInc = False

    def playerSlowDown(self):
        if self.pSpeedDec == False:
            self.usePowerUp = True
            self.pSpeedDec = True
            self.placeholder = self.playerSpeed
            self.playerSpeed = self.playerSpeed * 0.75
        else:
            self.usePowerUp = False
            self.playerSpeed = self.placeholder
            self.pSpeedDec = False

    def timerFired(self, dt):
        if self.timerCount % 600 == 0 and len(self.enemies) < self.enemyNum:
            self.enemies.append(Enemy(self.player, self.rootNode, \
                self.grid, self.dict, RED))
        if self.timerCount % 120 == 0:
            self.score += 1
            self.scoreList = self.text_format(str(self.score), font, 100, WHITE)
            self.scoreList_rect = self.scoreList.get_rect() 

        if self.timerCount % 600 == 0:
            self.spawnPowerUp()
            if len(self.powerups) > 5: 
                self.powerups = self.powerups[1:len(self.powerups)]

        if self.timeFreeze == False:
            for enemy in self.enemies:
                self.enemyMove(enemy)
        else:
            pass

        if self.usePowerUp == True:
            self.powerupTimer += 1
            if self.powerupTimer > self.fps * 5:
                self.powerupTimer = 0
                if self.timeFreeze == True:
                    self.timeFrozen()
                if self.pSpeedInc == True:
                    self.playerSpeedUp()
                if self.eSpeedDec == True:
                    self.enemySlowDown()
                if self.eSpeedInc == True:
                    self.enemySpeedUp()
                if self.pSpeedDec == True:
                    self.playerSpeedUp()

        self.playerMove() 
        self.timerCount += 1

        if self.grow == True:
            self.inner +=1
            if self.inner > 49:
                self.grow = False
        else:
            self.inner -= 1
            if self.inner < 26:
                self.grow = True

        for powerup in self.powerups:
            point = self.dict[powerup[0]]
            print(point[0] + self.scrollX, point[1] + self.scrollY)
            if math.isclose(point[0] + self.scrollX, self.width // 2, abs_tol = 3) and \
                math.isclose(point[1] + self.scrollY, self.height // 2, abs_tol = 3):
                # pause
                if self.usePowerUp == True:
                    pass
                else:
                    if powerup[1] == 0:
                        self.timeFrozen()
                    if powerup[1] == 1:
                        self.playerSpeedUp()
                    if powerup[1] == 2:
                        self.enemySlowDown()
                    if powerup[1] == 3:
                        self.enemySpeedUp()
                    if powerup[1] == 4:
                        self.playerSlowDown()
                    self.powerups.remove(powerup)

                    
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
            pygame.draw.circle(screen, RED, (int(enemy.currPos[0] +\
                self.scrollX), int(enemy.currPos[1] + self.scrollY)), 50)
            pygame.draw.circle(screen, BLACK, (int(enemy.currPos[0] +\
                self.scrollX), int(enemy.currPos[1] + self.scrollY)), self.inner)
            pygame.draw.circle(screen, RED, (int(enemy.currPos[0] +\
                self.scrollX), int(enemy.currPos[1] + self.scrollY)), self.inner - 25)

            if math.isclose(enemy.currPos[0] + self.scrollX, \
                self.width // 2, abs_tol = 10) \
                and math.isclose(enemy.currPos[1] + \
                self.scrollY, self.height // 2, abs_tol = 10):
                over = Gameover(self.score)
                try:
                    over.setDifficulty(self.difficulty)
                except:
                    pass
                over.run()

        if self.usePowerUp == True:
            pygame.draw.circle(screen, WHITE, (self.width // 2,\
                self.height//2), 50)
            pygame.draw.circle(screen, BLACK, (self.width // 2,\
                self.height//2), 47)
            for hour in range(12):
                cos = math.cos(math.radians(360.0 / 12 * hour))
                sin = math.sin(math.radians(360.0 / 12 * hour))
                x_h_0 = self.width/2 + 35*cos
                y_h_0 = self.height/2 + 35*sin
                x_h_1 = self.width/2 + 45*cos
                y_h_1 = self.height/2 + 45*sin
                pygame.draw.line(screen, WHITE, [x_h_0,y_h_0],[x_h_1,y_h_1],2)
                pygame.draw.line(screen, WHITE, (self.width // 2,\
                        self.height // 2), (self.width/2 + 45*math.cos\
                        (math.radians(360.0/(5*self.fps) * self.powerupTimer\
                        - 90)), self.height/2 + 45*math.sin(math.radians\
                        (360.0/(5*self.fps)* self.powerupTimer - 90))), 3)
        
        else:
            pygame.draw.circle(screen, BLACK, (self.width // 2,\
                self.height//2), 50)
            pygame.draw.circle(screen, WHITE, (self.width // 2,\
                self.height//2), self.inner)



        # displays powerups
        for powerup in self.powerups:
            if powerup[1] == 0:
                pygame.draw.rect(screen, WHITE, [self.dict[powerup[0]][0]\
                    - 25 + self.scrollX, self.dict[powerup[0]][1] - 25 + \
                    self.scrollY, 10, 50])
                pygame.draw.rect(screen, WHITE, [self.dict[powerup[0]][0] +\
                    15 + self.scrollX, self.dict[powerup[0]][1] - 25 + \
                    self.scrollY, 10, 50])

            if powerup[1] == 1:
                pygame.draw.polygon(screen, WHITE, [(self.dict[powerup[0]][0]\
                    + self.scrollX, self.dict[powerup[0]][1] + self.scrollY),\
                    (self.dict[powerup[0]][0] - 25 + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] - 25 + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])
                pygame.draw.polygon(screen, WHITE, [(self.dict[powerup[0]][0]\
                    + 25 + self.scrollX, self.dict[powerup[0]][1] + self\
                    .scrollY), (self.dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])
            
            if powerup[1] == 2:
                pygame.draw.polygon(screen, WHITE, [(self.dict[powerup[0]][0]\
                    - 25 + self.scrollX, self.dict[powerup[0]][1] + self\
                    .scrollY), (self.dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])

                pygame.draw.polygon(screen, WHITE, [(self.dict[powerup[0]][0]\
                    + self.scrollX, self.dict[powerup[0]][1] + self.scrollY)\
                    , (self.dict[powerup[0]][0] + 25 + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] + 25 + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])
            
            if powerup[1] == 3:
                pygame.draw.polygon(screen, RED, [(self.dict[powerup[0]][0]\
                    + self.scrollX, self.dict[powerup[0]][1] + self.scrollY),\
                    (self.dict[powerup[0]][0] - 25 + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] - 25 + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])
                pygame.draw.polygon(screen, RED, [(self.dict[powerup[0]][0]\
                    + 25 + self.scrollX, self.dict[powerup[0]][1] + self\
                    .scrollY), (self.dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])

            if powerup[1] == 4:
                pygame.draw.polygon(screen, RED, [(self.dict[powerup[0]][0]\
                    - 25 + self.scrollX, self.dict[powerup[0]][1] + self\
                    .scrollY), (self.dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])

                pygame.draw.polygon(screen, RED, [(self.dict[powerup[0]][0]\
                    + self.scrollX, self.dict[powerup[0]][1] + self.scrollY)\
                    , (self.dict[powerup[0]][0] + 25 + self.scrollX, self\
                    .dict[powerup[0]][1] - 25 + self.scrollY), (self\
                    .dict[powerup[0]][0] + 25 + self.scrollX, self\
                    .dict[powerup[0]][1] + 25 + self.scrollY)])

        screen.blit(self.scoreList, (self.width/2 - (self.scoreList_rect[2]/2), 20))
       
#creating and running the game
"""
def __init__(self, rootNode, playerSpeed, enemySpeed, enemyNum, width=600, \
            height=400,fps=50,title="GridLock")
"""

#game = gridLock(12, 6, 5, 4, 2000, 1200, 120)
#game.run()
