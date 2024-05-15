import pygame as pg
import math
import constants as c
from turret_data import TURRET_DATA


class Turret(pg.sprite.Sprite):
    def __init__(self,sprite_sheets,tile_x,tile_y, screen):
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 1
        self.range = TURRET_DATA[self.upgrade_level-1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level-1].get("cooldown")
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        self.tounge = 1
        self.last_tounge_pos = ()
        #positions vars
        self.tile_x = tile_x
        self.tile_y = tile_y
        #calculate center coords
        self.x = (self.tile_x +0.5) * c.TILE_SIZE
        self.y = (self.tile_y+0.5)* c.TILE_SIZE

        #animations vars
        self.screen = screen
        self.sprite_sheets = sprite_sheets
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()


        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        #create transparent circle showing range
        self.range_image = pg.Surface((self.range *2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "#d9bdc8", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
    
    def load_images(self, current_sheet):
        size = current_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = current_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self, enemy_group, world):
        #if target picked, play firin anim
        if self.target:
            self.play_animation()
        else:
            #search for new target once turret cooled down
            if pg.time.get_ticks() - self.last_shot > (self.cooldown / world.game_speed):

                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        #find an enemy to target
        x_dist = 0
        y_dist = 0
        #check if distance to each enemy is in range
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2+ y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.tounge = 1

                    self.target.health -= c.DAMAGE
                    break

    def play_animation(self):
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #check if animation is done
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                #record completed time and clear target
                self.last_shot = pg.time.get_ticks()
                self.image = self.animation_list[0]
                self.target = None

    def upgrade(self):
        self.upgrade_level += 1
        self.range = TURRET_DATA[self.upgrade_level-1].get("range")
        self.cooldown = TURRET_DATA[self.upgrade_level-1].get("cooldown")
        #upgraded turret image
        self.animation_list = self.load_images(self.sprite_sheets[self.upgrade_level - 1])
        self.image = self.animation_list[self.frame_index]
        #upgrade range circle
        self.range_image = pg.Surface((self.range *2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "#d9bdc8", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center
    
    def draw(self, surface):
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)
        if self.upgrade_level < 4:
            if self.target:
                self.draw_line_round_corners(self.screen, (self.x-10, self.y-10), self.target.pos, "#ea6262", 20)
            elif 1 - (self.tounge * 1.8) > 0.2:
                self.draw_retract_line_round_corners(self.screen, (self.x-10, self.y-10), self.last_tounge_pos, "#ea6262", 20)
            else:
                self.tounge = 1
        else:
            if self.target:
                self.draw_line_round_corners(self.screen, (self.x-10, self.y-10), self.target.pos, "#ff0034", 20)
                self.draw_line_round_corners(self.screen, (self.x - 10, self.y - 10), self.target.pos, "#ffdfe6", 10)
            elif 1 - (self.tounge * 1.8) > 0.3:
                self.draw_retract_line_round_corners(self.screen, (self.x-10, self.y-10), self.last_tounge_pos, "#ff0034", 20)
                self.draw_retract_line_round_corners(self.screen, (self.x - 10, self.y - 10), self.last_tounge_pos,
                                                     "#ffdfe6", 10)
            else:
                self.tounge = 1
            

    def draw_line_round_corners(self, surf, p1, p2, c, w):
        self.tounge = self.tounge * 0.8
        pg.draw.line(surf, c, p1, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w)
        pg.draw.circle(surf, c, p1, w / 2)
        pg.draw.circle(surf, c, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w / 2)
        self.last_tounge_pos =  (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge))
    
    def draw_retract_line_round_corners(self, surf, p1, p2, c, w):
        self.tounge = self.tounge * 1.8
        pg.draw.line(surf, c, p1, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w)
        pg.draw.circle(surf, c, p1, w / 2)
        pg.draw.circle(surf, c, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w / 2)
