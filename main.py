import pygame

from game_session import Session
from elements import Menu
from constans import *

pygame.init()

sc = pygame.display.set_mode((1000, 600), pygame.DOUBLEBUF)
pygame.display.set_caption("Спіймай всі")
pygame.display.set_icon(pygame.image.load("skin\\icon.png"))
clock = pygame.time.Clock()


menu = Menu()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            menu.mouse(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            map = menu.click(event.pos)
            if map:
                session = Session(sc, f"maps\\{map}")
                session.start_session()

    sc.blit(menu.get_menu(), (0, 0))
    pygame.display.update()

# 582121 (88, 33, 33)
# 624a27 (98, 74, 51)
# 234c25 (35, 76, 37)