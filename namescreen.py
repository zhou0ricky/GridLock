import pygame
import main
import gridLock
import menu
import string
from settingVars import settingVars
import leaderboard

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

class Namescreen(main.PygameGame):
# Text Renderer
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def init(self):
        self.bgColor = black
        self.score = settingVars.score
        self.name = self.text_format("Enter Name", font, 200, white)
        self.name_rect = self.name.get_rect()
        self.player = ""
        self.final = self.text_format(self.player, font, 200, white)
        self.final_rect = self.final.get_rect()

    def keyPressed(self, key, mod):
        if len(self.player) < 14: 
            if pygame.key.name(key) in string.ascii_letters or \
                pygame.key.name(key) in string.digits:
                self.player += pygame.key.name(key)
            elif key == pygame.K_SPACE:
                self.player += " "
        if key == pygame.K_BACKSPACE:
            self.player = self.player[:-1]
        self.final = self.text_format(self.player, font, 200, white)
        self.final_rect = self.final.get_rect()
        if key == pygame.K_RETURN:
            newscore = (self.player, self.score)
            leaderboard.addScores(newscore, settingVars.filename)
            board = leaderboard.Leaderboard(2000,1200)
            board.run()

    def redrawAll(self, screen):
        screen.blit(self.name, (self.width/2 -\
            self.name_rect[2]/2, 350))
        screen.blit(self.final, (self.width/2 -\
            (self.final_rect[2]/2) + 20, 600))

"""
def main():
    game = Namescreen(2000,1200)
    game.run()

if __name__=="__main__":
    main()
"""

    

    


