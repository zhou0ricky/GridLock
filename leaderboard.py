def checkHighscore(newScore, filename):
    file1 = open(filename, "r")
    text = file1.read()
    scores = []
    for line in text.splitlines():
        scores.append(tuple(line.split(",")))
    file1.close()
    print(scores)
    for pair in scores:
        if newScore > int(pair[1]):
            return True
    return False


def addScores(newScore, filename):
    file1 = open(filename, "r")
    text = file1.read()
    scores = []
    for line in text.splitlines():
        scores.append(tuple(line.split(",")))
    file1.close()

    if len(scores) == 0:
        scores.append(newScore)
    else:
        for i in range(len(scores)):
            if newScore[1] > int(scores[i][1]):
                scores = scores[0:i] + [newScore] + scores[i:10]
                break
    
    # converts tuples into string
    newScores =[]
    for pair in scores:
         newScores.append(str(pair[0]) + "," + str(pair[1]))

    scoreString = "\n".join(newScores)
    file1 = open(filename, "w")
    file1.write(scoreString)
    file1.close()

import pygame
import main
import menu
import gridLock
import difficulty
import gamemode
from settingVars import settingVars
# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "StressGenesis.otf"

class Leaderboard(main.PygameGame):

    # Text Renderer
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def init(self):
        self.bgColor = black
        self.select = 0
        self.title = self.text_format("High Scores",font, 150, white)
        self.title_rect=self.title.get_rect()
        self.ranking = self.text_format("Rank", font, 80, white)
        self.ranking_rect = self.ranking.get_rect()
        self.names = self.text_format("Player", font, 80, white)
        self.names_rect = self.names.get_rect()
        self.earning = self.text_format("Score", font, 80, white)
        self.earning_rect = self.earning.get_rect()
        self.setScores()

    def setScores(self):
        file1 = open(settingVars.filename, "r")
        text = file1.read()
        scores = []
        for line in text.splitlines():
            scores.append(tuple(line.split(",")))
        file1.close()

        self.rank = {}
        self.player = {}
        self.points = {}
        self.rank_rect = {}
        self.player_rect = {}
        self.points_rect = {}

        for i in range(10):
            self.rank[i] = self.text_format("{0}".format(i+1), font, 80, white)
            self.rank_rect[i] = self.rank[i].get_rect()
            self.player[i] = self.text_format(scores[i][0], font, 80, white)
            self.player_rect[i] = self.player[i].get_rect()
            self.points[i] = self.text_format(scores[i][1], font, 80, white)
            self.points_rect[i] = self.points[i].get_rect()

    def keyPressed(self, key, mod):
        if key == pygame.K_RETURN:
            home = menu.Menu(2000,1200)
            pygame.mixer.music.load("mainmusic.mp3")
            pygame.mixer.music.play(0)
            home.run()

    def redrawAll(self, screen):
        screen.blit(self.title, (self.width/2 - \
            (self.title_rect[2]/2), 50))
        screen.blit(self.ranking, (3 * (self.width/10) - \
            (self.ranking_rect[2]), 250))
        screen.blit(self.names, (6 * (self.width/10) - \
            (self.names_rect[2]), 250))
        screen.blit(self.earning, (8 * (self.width/10) - \
            (self.earning_rect[2]), 250))

        for i in range(10):
            screen.blit(self.rank[i], (3 * (self.width/10) - \
                (self.rank_rect[i][2]), 250 + ((i+1) * 80)))
            screen.blit(self.player[i], (6 * (self.width/10) - \
                (self.player_rect[i][2]), 250 + ((i+1) * 80)))
            screen.blit(self.points[i], (8 * (self.width/10) - \
                (self.points_rect[i][2]), 250 + ((i+1) * 80)))

     
"""
highscores = Leaderboard(2000, 1200)
highscores.run()
"""
