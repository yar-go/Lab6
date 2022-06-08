import os.path as path
from time import strftime, gmtime

import pygame

from constans import *

pygame.init()

class BeatMap:
    def __init__(self, dir_name):
        self.offset_time = 0
        self.f_audio = path.join(dir_name, 'audio.mp3')
        f_map = path.join(dir_name, 'map.level')
        pygame.mixer.music.load(self.f_audio)
        self.original_map = list()
        self.is_end = False

        try:
            with open(f_map, "r") as f:
                lines = f.readlines()
                self.map = list()
                for line in lines:
                    step = line.split(",")
                    self.map.append((int(step[0]), int(step[1]),))
                    self.original_map.append((int(step[0]), int(step[1]),))
        except FileNotFoundError:
            raise "BeatMap not found"

        self.duration = self.map[-1][0]

    def next_x(self):
        phase = (440/(FPS*FRUIT_SPEED))*1000
        position = pygame.mixer.music.get_pos() - self.offset_time
        if self.map:
            now = self.map[0]
            if now[0] < position + phase:
                return self.map.pop(0)[1]

        now_time = (pygame.mixer.music.get_pos() - self.offset_time)
        if (self.duration + 3000) < now_time:
            self.is_end = True
        return None

    def get_progress(self):
        now_time = (pygame.mixer.music.get_pos() - self.offset_time) // 1000
        last_time = (self.duration // 1000) + 3

        now_time = strftime("%M:%S", gmtime(now_time))
        last_time = strftime("%M:%S", gmtime(last_time))
        return f"{now_time}/{last_time}"

    def reset(self):
        self.offset_time = pygame.mixer.music.get_pos()
        self.map = self.original_map[:]
        pygame.mixer.music.rewind()

    def play_music(self):
        pygame.mixer.music.play(0)

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()
