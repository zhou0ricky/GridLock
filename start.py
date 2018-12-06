from menu import Menu
import pygame

def start():

    pygame.init()
    pygame.mixer.music.load("mainmusic.mp3")
    pygame.mixer.music.play(0)

    home = Menu(2000,1200)
    home.run()
    pygame.quit()

start()
