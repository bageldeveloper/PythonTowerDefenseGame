import pygame as pg
from enemy_data import ENEMY_SPAWN_DATA
import random
class World():
    def __init__(self, map_image):
        self.level = 1
        self.image = map_image
        self.enemy_list = []
        self.spawned_enemies = 0
    def draw(self, surface):
        surface.blit(self.image, (0,0))

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)