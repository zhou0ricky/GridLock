import pygame
import main


black = (0,0,0)
white = (255,255,255)
red = (255,0,0)


class Gameover(main.PygameGame):
    @staticmethod
    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def message_display(self, screen ,text):
        largeText = pygame.font.Font('freesansbold.ttf',75)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = (self.width // 2, self.height // 2)
        screen.blit(TextSurf, TextRect) 
    
    def redrawAll(self, screen):
        self.message_display(screen, 'GAME OVER') 

