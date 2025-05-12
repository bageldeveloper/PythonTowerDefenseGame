import pygame as pg
from pygame.math import Vector2
import math
import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type, waypoints, images, screen):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.reward = ENEMY_DATA.get(enemy_type)["reward"]
        self.angle = 0
    

        self.screen = screen
        self.animation_list = self.load_images(images.get(enemy_type))
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()


        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        
    def load_images(self, current_sheet):
        size = current_sheet.get_height()
        animation_list = []
        sheet_width = current_sheet.get_width()
        for x in range(c.ENEMY_ANIMATION_STEPS):
            if (x + 1) * size <= sheet_width:  # Changed the condition to allow for correct slicing
                try:
                    temp_img = current_sheet.subsurface(pg.Rect(x * size, 0, size, size))
                    animation_list.append(temp_img)
                except ValueError as e:
                    print(f"Error loading image at index {x}: {e}")
                    break
            else:
                break

        return animation_list

    def update(self, world):
      
        self.check_alive(world)
        self.play_animation()
        self.move(world)
        self.rotate()

    def move(self, world):
        # define target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # enemy is at end of path, it has served its purpose and must be eliminated
            world.health -= 1
            world.missed_enemies += 1
            self.kill()
        # calculate distance to target hehe
        dist = self.movement.length()
        # check if remaining is greater that speed
        if dist > (self.speed * world.game_speed):
            self.pos += self.movement.normalize() * (self.speed * world.game_speed)
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1
            if self.target_waypoint < len(self.waypoints):
                self.target = Vector2(self.waypoints[self.target_waypoint])
                self.movement = self.target - self.pos

    def rotate(self):
        # calculate distance to next waypoint
        dist = self.target - self.pos
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # rotate image and rectangle
        # self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.angle <= -90:
            self.image = pg.transform.flip(self.image, True, False)
        elif dist[0]+dist[1] != 0:
            self.image = pg.transform.flip(self.image, False, False)
    def check_alive(self, world):
        if self.health <= 0:
            upgrade_sound = pg.mixer.Sound("assets/audio/sfx/flydie.wav")
            pg.mixer.Sound.play(upgrade_sound)

            world.killed_enemies += 1
            world.money += c.KILL_REWARD
            self.kill()

    def play_animation(self):
        #update image
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed
        if pg.time.get_ticks() - self.update_time > c.ENEMY_ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            #check if animation is done
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                #record completed time and clear target
                self.last_shot = pg.time.get_ticks()
                self.image = self.animation_list[0]
                self.target = None

