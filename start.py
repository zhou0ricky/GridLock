from menu import Menu
import pygame

def start():

    pygame.init()
    #CITATION: I got this from https://www.youtube.com/watch?v=n-aitfK7jRE
    pygame.mixer.music.load("mainmusic.mp3")
    pygame.mixer.music.play(0)

    home = Menu(2000,1200)
    home.run()
    pygame.quit()

start()
