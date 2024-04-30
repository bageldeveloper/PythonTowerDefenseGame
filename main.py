import pygame as pg
from enemy import Enemy
from world import World
import constants as c

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

pg.display.set_caption("Tower Defense")

#LOAD IMAGES

map_image = pg.image.load('assets/images/levels/map.png').convert_alpha()

overlay_map_image = pg.image.load('assets/images/levels/mapoverlay.png').convert_alpha()

enemy_image = pg.image.load('assets/images/enemies/fly.png').convert_alpha()

enemy_image = pg.transform.scale(enemy_image, (80,80))

map_image = pg.transform.scale(map_image, (880,880))

overlay_map_image = pg.transform.scale(overlay_map_image, (880,880))

#CREATE WORLD
world = World(map_image)

overlay = World(overlay_map_image)

#CREATE GROUPS

enemy_group = pg.sprite.Group()

waypoints = [
    (680,0),
    (680,100),
    (460,100),
    (460,180),
    (120,180),
    (120,420),
    (360,420),
    (360,340),
    (460,340)
]

enemy = Enemy(waypoints, enemy_image)

enemy_group.add(enemy)

run = True

while run:

    clock.tick(c.FPS)

    screen.fill("grey")

    #draw level

    world.draw(screen)

    pg.draw.lines(screen, "black", False, waypoints)
    enemy_group.update()
    enemy_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    overlay.draw(screen)
    pg.display.flip()

pg.quit()
