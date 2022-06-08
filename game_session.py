import pygame

from elements import Player, Fruit, Rating, MusicProgress, PauseMenu, GameEnd
from map_loader import BeatMap
from constans import *

pygame.init()


class Session:
    def __init__(self, screen, beat_map):
        self.sc = screen
        self.map = beat_map
        self.fruit_skins = [pygame.image.load(f"skin\\game\\f{i}.png").convert_alpha() for i in range(1, 5)]
        self.player_group = pygame.sprite.Group()
        self.player_group.add(Player(W, H))
        self.fruits = pygame.sprite.Group()
        self.b_map = BeatMap(beat_map)
        self.b_map.play_music()
        self.m_progress = MusicProgress(self.b_map)
        self.rating = Rating()
        self.h = pygame.mixer.Sound("skin\\audio\\hit.ogg")
        self.f = pygame.mixer.Sound("skin\\audio\\fail.ogg")
        self.h.set_volume(0.2)
        self.f.set_volume(1)
        self.pause_game = PauseMenu(W, H, self.b_map, self.rating)
        self.end_menu = GameEnd(self.rating, self.map)
        pygame.mouse.set_visible(False)

    def fruit_catch(self):
        if self.fruits.sprites():
            fruits = self.fruits.sprites()[0:5]
            for fruit in fruits:
                if self.player_group.sprites()[0].rect.collidepoint(fruit.rect.center):
                    fruit.kill()
                    self.rating.up_combo()
                    self.rating.add_rating()
                    self.h.play(0)

    def fruit_not_catch(self):
        self.rating.down_combo()
        self.rating.add_rating()
        self.f.play(0)

    def generate_fruits(self):
        next_fruit_x = self.b_map.next_x()
        if next_fruit_x:
            self.fruits.add(Fruit(next_fruit_x, W, H, self.fruit_skins, self.fruit_not_catch))

    def draw_end(self, pos=None):
        if self.end_menu:
            self.sc.blit(self.end_menu.get_screen(pos), (0, 0))
            pygame.display.update()

    def start_session(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.mouse.set_visible(True)
                    self.b_map.pause_music()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.pause_game.pause:
                            self.pause_game.pause = True
                        else:
                            self.pause_game.pause = False
                            pygame.mouse.set_visible(False)
                            self.b_map.unpause_music()
                if event.type == pygame.MOUSEMOTION and self.pause_game.pause:
                    self.pause_game.mouse(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and self.pause_game.pause:
                    self.pause_game.click(event.pos)

                if event.type == pygame.MOUSEMOTION and self.end_menu.is_end:
                    self.draw_end(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and self.end_menu.is_end:
                    self.end_menu.click(event.pos)

            if self.pause_game.pause:
                if self.pause_game.done:
                    return
                self.sc.blit(self.pause_game.get_pause(), (0, 0))
                pygame.display.update()
                continue

            if self.end_menu.is_end:
                if self.end_menu.done:
                    return
                self.draw_end()
                continue

            if self.b_map.is_end:
                self.end_menu.is_end = True
                continue

            self.generate_fruits()
            self.fruit_catch()
            self.sc.fill(BLACK)
            self.sc.blit(self.rating.get_rating(), (0, 0))
            self.sc.blit(self.m_progress.get_screen(), (W - 160, 0))
            self.player_group.update()
            self.fruits.update()
            self.fruits.draw(self.sc)
            self.player_group.draw(self.sc)

            pygame.display.update()
