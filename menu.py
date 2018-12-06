import pygame
import main
import gridLock
import difficulty
import gamemode

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


class Menu(main.PygameGame):
        
    # Text Renderer
    @staticmethod
    def text_format(message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)
        
        return newText
       
    def init(self):
        self.bgColor = black
        self.select = 0
        self.title = self.text_format("GridLock",font, 200, white)
        self.title_rect=self.title.get_rect()
        self.play = self.text_format("Play", font, 80, black)
        self.play_rect = self.play.get_rect()
        self.gamemode = self.text_format("Gamemode", font, 80, white)
        self.gamemode_rect = self.gamemode.get_rect()
        self.settings = self.text_format("Settings", font, 80, white)
        self.settings_rect = self.settings.get_rect()

    def setDifficulty(self, mode):
        self.difficulty = mode

    def setGamemode(self, mode):
        self.gamemode = mode
        
    def keyPressed(self, key, mod):
        if key == pygame.K_UP:
            self.select = (self.select - 1) % 3
        if key == pygame.K_DOWN:
            self.select = (self.select + 1) % 3
        if key == pygame.K_RETURN and self.select == 0:
            game = gridLock.gridLock(10, 8, 6, 5, 2000, 1200, 150)  
            game.run()
        if key == pygame.K_RETURN and self.select == 1:
            mode = gamemode.Gamemode(2000,1200)
            mode.run()
        if key == pygame.K_RETURN and self.select == 2:
            scale = difficulty.Difficulty(2000,1200)
            scale.run()
        if key == pygame.K_ESCAPE:
            quit()


        self.setMode()

    def setMode(self):
        if self.select == 0:
            self.play = self.text_format("Play", font, 80, black)
        else:
            self.play = self.text_format("Play", font, 80, white)
        self.play_rect = self.play.get_rect()
        
        if self.select == 1:
            self.gamemode = self.text_format("Gamemode", font, 80, black)
        else:
            self.gamemode = self.text_format("Gamemode", font, 80, white)
        self.gamemode_rect = self.gamemode.get_rect()

        if self.select == 2:
            self.settings = self.text_format("Settings", font, 80, black)
        else:
            self.settings = self.text_format("Settings", font, 80, white)
        self.settings_rect = self.settings.get_rect()

    def redrawAll(self, screen):
        screen.blit(self.title, (self.width/2 -\
            (self.title_rect[2]/2), self.height // 6))
        
        if self.select == 0:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.play_rect[2]/2 - 10 ,442,self.play_rect[2] + 10,100], 0)

        if self.select == 1:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.gamemode_rect[2]/2 - 10,592,\
                self.gamemode_rect[2]+ 10 ,100], 0)

        if self.select == 2:
            pygame.draw.rect(screen, white, [self.width/2 - \
                self.settings_rect[2]/2-10,742,self.settings_rect[2]+10,100], 0)

        screen.blit(self.play, (self.width/2 - (self.play_rect[2]/2), 450))
        
        screen.blit(self.gamemode, (self.width/2 - \
            (self.gamemode_rect[2]/2), 600))

        screen.blit(self.settings, (self.width/2 - \
            (self.settings_rect[2]/2), 750))
"""        
def main():
    menu = Menu(2000,1200)
    menu.run()

if __name__ == '__main__':
    main()
"""
