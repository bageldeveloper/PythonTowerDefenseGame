import pygame as pg
import math
import constants as c


class Turret(pg.sprite.Sprite):
    def __init__(self,sprite_sheet,tile_x,tile_y, screen):
        pg.sprite.Sprite.__init__(self)
        self.range = 120
        self.cooldown = 1500
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
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
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
    
    def load_images(self):
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list
    
    def update(self, enemy_group):
        #if target picked, play firin anim
        if self.target:
            self.play_animation()
        else:
            #search for new target once turret cooled down
            if pg.time.get_ticks() - self.last_shot > self.cooldown:

                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        #find an enemy to target
        x_dist = 0
        y_dist = 0
        #check if distance to each enemy is in range
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[0] - self.y
            dist = math.sqrt(x_dist ** 2+ y_dist ** 2)
            if dist < self.range:
                self.target = enemy
                self.tounge = 1

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
    
    def draw(self, surface):
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)
        if self.target:
            self.draw_line_round_corners(self.screen, (self.x-10, self.y-10), self.target.pos, "#ea6262", 20)
        elif 1 - self.tounge * 1.8 > 0.1:
            self.draw_retract_line_round_corners(self.screen, (self.x-10, self.y-10), self.last_tounge_pos, "#ea6262", 20)
            

    def draw_line_round_corners(self, surf, p1, p2, c, w):
        self.tounge = self.tounge * 0.8
        pg.draw.line(surf, c, p1, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w)
        pg.draw.circle(surf, c, p1, w // 2)
        pg.draw.circle(surf, c, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w // 2)
        self.last_tounge_pos =  (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge))
    
    def draw_retract_line_round_corners(self, surf, p1, p2, c, w):
        self.tounge = self.tounge * 1.8
        pg.draw.line(surf, c, p1, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w)
        pg.draw.circle(surf, c, p1, w // 2)
        pg.draw.circle(surf, c, (p1[0] + (p2[0] - p1[0]) * (1 - self.tounge), p1[1] + (p2[1] - p1[1]) * (1 - self.tounge)), w // 2)
