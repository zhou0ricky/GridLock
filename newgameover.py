import pygame
import main
import gridLock
import menu
from settingVars import settingVars
from namescreen import Namescreen

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

class NewGameover(main.PygameGame):
# Text Renderer
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def init(self):
        self.score = settingVars.score
        self.bgColor = black
        self.new = self.text_format("Score", font, 150, white)
        self.new_rect = self.new.get_rect()
        self.high = self.text_format(str(self.score), font, 600, white)
        self.high_rect = self.high.get_rect()
        self.points = self.text_format("New High Score", font, 200, white)
        self.points_rect = self.points.get_rect()
        self.truth = True
        self.shrink = 0

    def keyPressed(self, key, mod):
        if key == pygame.K_RETURN:
            screen = Namescreen(2000,1200)
            screen.run()
            

    def timerFired(self, dt):
        if self.truth == True:
            self.shrink += 1
            if self.shrink > 50:
                self.truth = False
        else:
            self.shrink -= 1
            if self.shrink < 0:
                self.truth = True
        self.new = self.text_format("Score", font, 150 - self.shrink, white)
        self.new_rect = self.new.get_rect()
        self.high = self.text_format(str(self.score), font, 600 - 2 * self.shrink, white)
        self.high_rect = self.high.get_rect()
        self.points = self.text_format("New High Score", font, 200 - self.shrink, white)
        self.points_rect = self.points.get_rect()


    def redrawAll(self, screen):
        screen.blit(self.new, (self.width/2 -\
            self.new_rect[2]/2 - 10, 200 - self.shrink))
        screen.blit(self.high, (self.width/2 -\
            self.high_rect[2]/2, 300 - self.shrink))
        screen.blit(self.points, (self.width/2 -\
            self.points_rect[2]/2, 850 -2* self.shrink))

def main():
    game = NewGameover(2000,1200)
    game.run()

if __name__ == '__main__':
    main()

