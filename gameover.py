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
# CITATION: I got this from https://www.fontsquirrel.com/
font = "StressGenesis.otf"

#CITATION: I got this from https://qwewy.gitbooks.io/pygame-module-manual/chapter1/framework.html
class Gameover(main.PygameGame):
# Text Renderer
    #CITATION: I got this code from https://nerdparadise.com/programming/pygame/part5
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)

        return newText

    def init(self):
        self.score = settingVars.score
        self.bgColor = black
        self.title = self.text_format("Score:", font, 200, white)
        self.title_rect = self.title.get_rect()
        self.final = self.text_format(str(self.score), font, 800, white)
        self.final_rect = self.final.get_rect()
        self.again = self.text_format("Again", font, 100, black)
        self.again_rect = self.again.get_rect()
        self.exit = self.text_format("Exit", font, 100, white)
        self.exit_rect = self.exit.get_rect()
        self.select = 0

    def keyPressed(self, key, mod):
        if key == pygame.K_LEFT:
            self.select = (self.select - 1) % 2
        if key == pygame.K_RIGHT:
            self.select = (self.select + 1) % 2
        if key == pygame.K_RETURN and self.select == 0:
            game = gridLock.gridLock(10, 8, 6, 5, 2000, 1200, 150)
            game.run()
        if key == pygame.K_RETURN and self.select == 1:
            #CITATION: I got this from https://www.youtube.com/watch?v=n-aitfK7jRE
            pygame.mixer.music.load("mainmusic.mp3")
            pygame.mixer.music.play(0)
            home = menu.Menu(2000,1200)
            home.run()

        self.setMode()

    def setMode(self):
        if self.select == 0:
            self.again = self.text_format("Again", font, 100, black)
        else:
            self.again = self.text_format("Again", font, 100, white)
        self.again_rect = self.again.get_rect()

        if self.select == 1:
            self.exit = self.text_format("Exit", font, 100, black)
        else:
            self.exit = self.text_format("Exit", font, 100, white)
        self.exit_rect = self.exit.get_rect()

    def redrawAll(self, screen):
        screen.blit(self.title, (self.width/2 -\
            self.title_rect[2]/2, 100))
        screen.blit(self.final, (self.width/2 -\
            (self.final_rect[2]/2) + 20, 200)) 

        if self.select == 0:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.again_rect[2]/2 - 260 ,950 ,self.again_rect[2] + 20,100], 0)

        if self.select == 1:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.exit_rect[2]/2 +240,950,\
                self.exit_rect[2]+ 10 ,100], 0)

        screen.blit(self.again, (self.width/2 - self.again_rect[2] -120, 950)) 
        screen.blit(self.exit, (self.width/2 + 160, 950))
 
def main():
    game = Gameover(8)
    game.run()

if __name__ == '__main__':
    main()

    
    
