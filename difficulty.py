import pygame 
import main
import gridLock
import menu
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


class Difficulty(main.PygameGame):
    # Text Renderer
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def init(self):
        self.bgColor = black
        self.select = 0 
        self.difficulty = self.text_format("Select Difficulty", font,175,white)
        self.difficulty_rect = self.difficulty.get_rect()
        self.easy=self.text_format("Easy",font,100,black)
        self.easy_rect=self.easy.get_rect()
        self.medium=self.text_format("Medium",font,100,white)
        self.medium_rect=self.medium.get_rect()
        self.CMU=self.text_format("CMU",font,100,white)
        self.CMU_rect=self.CMU.get_rect()
        """
        self.back=self.text_format("Back",font,100,white)
        self.back_rect=self.back.get_rect()
        """

    def keyPressed(self, key, mod):
        if key == pygame.K_UP:
            self.select = (self.select - 1) % 3
        if key == pygame.K_DOWN:
            self.select = (self.select + 1) % 3
        if key == pygame.K_RETURN and self.select == 0:
            home = menu.Menu(2000,1200)
            settingVars.difficulty = 0
            home.run()
        if key == pygame.K_RETURN and self.select == 1:
            home = menu.Menu(2000,1200)
            settingVars.difficulty = 1
            home.run()
        if key == pygame.K_RETURN and self.select == 2:
            home = menu.Menu(2000,1200)
            settingVars.difficulty = 2
            home.run()
        """
        if key == pygame.K_RETURN and self.select == 3:
            home = menu.Menu(2000,1200)
            home.run()
        """

        self.setMode()

    def setMode(self):
        if self.select == 0:
            self.easy = self.text_format("Easy", font, 100, black)
        else:
            self.easy = self.text_format("Easy", font, 100, white)
        self.easy_rect = self.easy.get_rect()

        if self.select == 1:
            self.medium = self.text_format("Medium", font, 100, black)
        else:
            self.medium = self.text_format("Medium", font, 100, white)
        self.medium_rect = self.medium.get_rect()

        if self.select == 2:
            self.CMU = self.text_format("CMU", font, 100, black)
        else:
            self.CMU = self.text_format("CMU", font, 100, white)
        self.CMU_rect = self.CMU.get_rect()

        """
        if self.select == 3:
            self.back = self.text_format("Back", font, 100, black)
        else:
            self.back = self.text_format("Back", font, 100, white)
        self.back_rect = self.back.get_rect()
        """


    def redrawAll(self, screen):
        screen.blit(self.difficulty, (self.width/2 -\
            (self.difficulty_rect[2]/2), 200))

        if self.select == 0:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.easy_rect[2]/2 - 10 ,450,self.easy_rect[2] + 10,100], 0)

        if self.select == 1:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.medium_rect[2]/2 - 10,600,\
                self.medium_rect[2]+ 10 ,100], 0)

        if self.select == 2:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.CMU_rect[2]/2-10,750,self.CMU_rect[2]+10,100], 0)

        """
        if self.select == 3:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.back_rect[2]/2-10,950,self.back_rect[2]+10,100], 0)
        """

        screen.blit(self.easy, (self.width/2 - (self.easy_rect[2]/2), 450))

        screen.blit(self.medium, (self.width/2 - \
            (self.medium_rect[2]/2), 600))

        screen.blit(self.CMU, (self.width/2 - \
            (self.CMU_rect[2]/2), 750))

        """
        screen.blit(self.back, (self.width/2 - \
            (self.back_rect[2]/2), 950))
        """

"""
def main():
    difficulty = Difficulty(2000,1200)
    difficulty.run()

if __name__=='__main__':
    main()
"""

