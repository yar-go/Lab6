import random

import pygame

from constans import *


class Player(pygame.sprite.Sprite):
    def __init__(self, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("skin/game\\player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(w // 2, h+60))
        self.move_speed = 10

    def update(self, *args):
        keys = pygame.key.get_pressed()
        speed = self.move_speed
        if keys[pygame.K_l]:
            speed *= 2
        if keys[pygame.K_a]:
            if not self.rect.left <= 0:
                self.rect.x -= speed
        elif keys[pygame.K_s]:
            if not self.rect.right >= 1000:
                self.rect.x += speed


class Fruit(pygame.sprite.Sprite):
    def __init__(self, x:int, w:int, h:int, skin:list, callback=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(skin)

        phase = (w - 640) // 2
        self.rect = self.image.get_rect(center=(x+phase, -10))
        self.h = h
        self.speed = FRUIT_SPEED
        self.anti = callback

    def update(self):
        self.rect.y += self.speed
        if self.rect.top - 100 == self.h:
            if self.anti:
                self.anti()
            self.kill()


class Rating:
    def __init__(self):
        self.combo = 1
        self.rating = 0
        self.max_combo = 0
        self.text_generator = pygame.font.SysFont("Impact", 32, False)
        self.surf = pygame.surface.Surface((320, 320))

    def get_rating(self):
        self.surf.fill(BLACK)
        rating = self.text_generator.render(f"{self.rating}", 1, WHITE, BLACK)
        combo = self.text_generator.render(f"x{self.combo}", 1, WHITE, BLACK)
        self.surf.blit(rating, (0, 0))
        self.surf.blit(combo, (0, 35))
        return self.surf

    def add_rating(self):
        self.rating += self.combo

    def up_combo(self):
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo

    def down_combo(self):
        self.combo = 1

    def reset(self):
        self.rating = 0
        self.max_combo = 0
        self.combo = 0

    def __repr__(self):
        return f"{self.rating}  {self.combo}"


class MusicProgress:
    def __init__(self, beatmap):
        self.beatmap = beatmap
        self.text_generator = pygame.font.SysFont("Impact", 30, False)
        self.surf = pygame.surface.Surface((180, 32))

    def get_screen(self):
        self.surf.fill(BLACK)
        text = self.beatmap.get_progress()
        item = self.text_generator.render(text, True, WHITE, BLACK)
        self.surf.blit(item, (0, 0))
        return self.surf


class PauseMenu:
    def __init__(self, W, H, beatmap, progres):
        self.text_generator = pygame.font.SysFont("Impact", 30, False)
        self.surf = pygame.surface.Surface((W, H+100))
        self.beatmap = beatmap
        self._pause = False
        self.mouse_on_m = 0
        self.done = False
        self.progres = progres

        self.backgroud = pygame.image.load("skin\\pause\\pause-overlay.png").convert_alpha()
        self.backgroud_rect = self.backgroud.get_rect(topleft=(0, 0))

        self.resume = pygame.image.load("skin\\pause\\pause-continue.png").convert_alpha()
        self.resume_rect = self.resume.get_rect(center=(500, 100))
        self.resume2 = pygame.transform.scale(self.resume, (293, 185))

        self.retry = pygame.image.load("skin\\pause\\pause-retry.png").convert_alpha()
        self.retry_rect = self.retry.get_rect(center=(500, 267))
        self.retry2 = pygame.transform.scale(self.retry, (296, 127))

        self.back = pygame.image.load("skin\\pause\\pause-back.png").convert_alpha()
        self.back_rect = self.back.get_rect(center=(500, 430))
        self.back2 = pygame.transform.scale(self.back, (293, 185))

        self.hover_s = pygame.mixer.Sound("skin\\audio\\hover.ogg")
        self.click_s = pygame.mixer.Sound("skin\\audio\\click.ogg")

    @property
    def pause(self):
        return self._pause

    @pause.setter
    def pause(self, value):
        self._pause = value
        if value:
            pygame.mouse.set_visible(True)
            self.beatmap.pause_music()
        else:
            pygame.mouse.set_visible(False)
            self.beatmap.unpause_music()

    def mouse(self, position):
        prev = self.mouse_on_m
        if self.resume_rect.collidepoint(*position):
            self.mouse_on_m = 1
        elif self.retry_rect.collidepoint(*position):
            self.mouse_on_m = 2
        elif self.back_rect.collidepoint(*position):
            self.mouse_on_m = 3
        else:
            self.mouse_on_m = 0

        if not prev == self.mouse_on_m:
            self.hover_s.play(0)

    def get_pause(self):
        self.surf.fill(BLACK)
        self.surf.blit(self.backgroud, self.backgroud_rect)

        if self.mouse_on_m == 1:
            self.surf.blit(self.resume2, self.resume_rect)
            self.surf.blit(self.retry, self.retry_rect)
            self.surf.blit(self.back, self.back_rect)
        elif self.mouse_on_m == 2:
            self.surf.blit(self.resume, self.resume_rect)
            self.surf.blit(self.retry2, self.retry_rect)
            self.surf.blit(self.back, self.back_rect)
        elif self.mouse_on_m == 3:
            self.surf.blit(self.resume, self.resume_rect)
            self.surf.blit(self.retry, self.retry_rect)
            self.surf.blit(self.back2, self.back_rect)
        else:
            self.surf.blit(self.resume, self.resume_rect)
            self.surf.blit(self.retry, self.retry_rect)
            self.surf.blit(self.back, self.back_rect)

        return self.surf

    def click(self, mouse_position):
        self.click_s.play(0)
        if self.resume_rect.collidepoint(*mouse_position):
            self.pause = False
        elif self.retry_rect.collidepoint(*mouse_position):
            self.beatmap.reset()
            self.progres.reset()
            self.pause = False
        elif self.back_rect.collidepoint(*mouse_position):
            self.done = True
        else:
            pass


class GameEnd:
    def __init__(self, rating, level):
        self.text_generator = pygame.font.SysFont("Impact", 30, False)
        self.surf = pygame.surface.Surface((W, H+100))
        self.rating = rating
        self.level = level
        self._is_end = False
        self.back_imgs = [pygame.image.load(f"skin\\back\\menu-back-{i}.png").convert_alpha() for i in range(180)]
        self.back_img_num = 0
        self.back_b_rect = self.back_imgs[0].get_rect(bottomleft=(0, 600))
        self.done = False

        self.hover_s = pygame.mixer.Sound("skin\\audio\\hover.ogg")
        self.click_s = pygame.mixer.Sound("skin\\audio\\click.ogg")

    @property
    def is_end(self):
        return self._is_end

    @is_end.setter
    def is_end(self, value):
        self._is_end = value
        if value:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def get_screen(self, mouse_position=None):
        pygame.mouse.set_visible(True)
        self.surf.fill(BLACK)
        score = self.text_generator.render(f"Score: {str(self.rating.rating)}", True, WHITE, BLACK)
        combo = self.text_generator.render(f"Combo: {str(self.rating.max_combo)}", True, WHITE, BLACK)
        score_rect = score.get_rect(center=(500, 250))
        combo_rect = combo.get_rect(center=(500, 350))
        self.surf.blit(score, score_rect)
        self.surf.blit(combo, combo_rect)
        if self.back_img_num == 180:
            self.back_img_num = 0
        self.surf.blit(self.back_imgs[self.back_img_num], self.back_b_rect)
        self.back_img_num += 1
        return self.surf

    def click(self, mouse_position):
        self.click_s.play(0)
        if self.back_b_rect.collidepoint(*mouse_position):
            self.done = True

class Menu:
    def __init__(self):
        self.backgroud = ((35, 76, 37), (98, 74, 51), (88, 33, 33))
        self.status_menu = 0
        self.maps = ["easy", "middle", "hard"]

        self.easy_i = pygame.image.load("skin\\menu\\easy.png").convert_alpha()
        self.middle_i = pygame.image.load("skin\\menu\\middle.png").convert_alpha()
        self.hard_i = pygame.image.load("skin\\menu\\hard.png").convert_alpha()

        self.easy_t = pygame.image.load("skin\\menu\\easy-text.png").convert_alpha()
        self.middle_t = pygame.image.load("skin\\menu\\middle-text.png").convert_alpha()
        self.hard_t = pygame.image.load("skin\\menu\\hard-text.png").convert_alpha()

        self.e_i = self.easy_i.get_rect(center=(370, 150))
        self.m_i = self.middle_i.get_rect(center=(370, 300))
        self.h_i = self.hard_i.get_rect(center=(370, 450))
        self.e_t = self.easy_i.get_rect(midleft=(434, 150))
        self.m_t = self.middle_t.get_rect(midleft=(434, 300))
        self.h_t = self.hard_t.get_rect(midleft=(434, 450))

        self.e_t_m = self.easy_i.get_rect(midleft=(434+20, 150))
        self.m_t_m = self.middle_t.get_rect(midleft=(434+20, 300))
        self.h_t_m = self.hard_t.get_rect(midleft=(434+20, 450))

        self.hover_s = pygame.mixer.Sound("skin\\audio\\hover.ogg")
        self.click_s = pygame.mixer.Sound("skin\\audio\\click.ogg")

        self.surf = pygame.surface.Surface((W, H + 100))

    def mouse(self, position):
        prev_status = self.status_menu
        if self.e_i.collidepoint(*position) or self.e_t.collidepoint(*position):
            self.status_menu = 0
        elif self.m_i.collidepoint(*position) or self.m_t.collidepoint(*position):
            self.status_menu = 1
        elif self.h_i.collidepoint(*position) or self.h_t.collidepoint(*position):
            self.status_menu = 2

        if not prev_status == self.status_menu:
            self.hover_s.play(0)

    def click(self, position):
        self.click_s.play(0)
        if self.e_i.collidepoint(*position) or self.e_t.collidepoint(*position):
            pass
        elif self.m_i.collidepoint(*position) or self.m_t.collidepoint(*position):
            pass
        elif self.h_i.collidepoint(*position) or self.h_t.collidepoint(*position):
            pass
        else:
            return None

        return self.maps[self.status_menu]

    def get_menu(self):
        self.surf.fill(self.backgroud[self.status_menu])

        self.surf.blit(self.easy_i, self.e_i)
        self.surf.blit(self.middle_i, self.m_i)
        self.surf.blit(self.hard_i, self.h_i)

        if self.status_menu == 0:
            x,y = self.e_t.center
            self.surf.blit(self.easy_t, self.e_t_m)
            self.surf.blit(self.middle_t, self.m_t)
            self.surf.blit(self.hard_t, self.h_t)
        elif self.status_menu == 1:
            self.surf.blit(self.easy_t, self.e_t)
            self.surf.blit(self.middle_t, self.m_t_m)
            self.surf.blit(self.hard_t, self.h_t)
        elif self.status_menu == 2:
            self.surf.blit(self.easy_t, self.e_t)
            self.surf.blit(self.middle_t, self.m_t)
            self.surf.blit(self.hard_t, self.h_t_m)
        else:
            self.surf.blit(self.easy_t, self.e_t)
            self.surf.blit(self.middle_t, self.m_t)
            self.surf.blit(self.hard_t, self.h_t)

        return self.surf