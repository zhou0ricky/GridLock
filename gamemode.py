import pygame 
import main
import gridLock
import menu
from settingVars import settingVars

# Colors
white=(253, 245, 230)
black=(15, 15, 15)
gray=(50, 50, 50) 
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
 
# Game Fonts
#CITATION: I got this from https://www.fontsquirrel.com/
font = "StressGenesis.otf"


#CITATION: I got this from https://qwewy.gitbooks.io/pygame-module-manual/chapter1/framework.html
class Gamemode(main.PygameGame):
    # Text Renderer
    #CITATION: I got this code from https://nerdparadise.com/programming/pygame/part5
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def init(self): 
        self.bgColor = black
        self.select = 0
        self.mode = self.text_format("Select Mode", font,175,white)
        self.mode_rect = self.mode.get_rect()
        self.survival=self.text_format("Survival",font,100,black)
        self.survival_rect=self.survival.get_rect()
        self.arcade=self.text_format("Arcade",font,100,white)
        self.arcade_rect=self.arcade.get_rect()

    def keyPressed(self, key, mod):
        if key == pygame.K_UP:
            self.select = (self.select - 1) % 2
        if key == pygame.K_DOWN:
            self.select = (self.select + 1) % 2
        if key == pygame.K_RETURN and self.select == 0:
            home = menu.Menu(2000,1200)
            settingVars.gameMode = 0
            home.run()
        if key == pygame.K_RETURN and self.select == 1:
            home = menu.Menu(2000,1200)
            settingVars.gameMode = 1
            home.run()

        self.setMode()

    def setMode(self):
        if self.select == 0:
            self.survival = self.text_format("Survival", font, 100, black)
        else:
            self.survival = self.text_format("Survival", font, 100, white)
        self.survival_rect = self.survival.get_rect()

        if self.select == 1:
            self.arcade = self.text_format("Arcade", font, 100, black)
        else:
            self.arcade = self.text_format("Arcade", font, 100, white)
        self.arcade_rect = self.arcade.get_rect()

       
    def redrawAll(self, screen):
        screen.blit(self.mode, (self.width/2 -\
            (self.mode_rect[2]/2), 300))

        if self.select == 0:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.survival_rect[2]/2 - 10 ,550,self.survival_rect[2] + 10,100], 0)

        if self.select == 1:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.arcade_rect[2]/2 - 10,700,\
                self.arcade_rect[2]+ 10 ,100], 0)

        screen.blit(self.survival, (self.width/2 - (self.survival_rect[2]/2), 550))

        screen.blit(self.arcade, (self.width/2 - \
            (self.arcade_rect[2]/2), 700))


def main():
    mode = Gamemode(2000,1200)
    mode.run()

if __name__=='__main__':
    main()
