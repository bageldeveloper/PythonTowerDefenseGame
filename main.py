import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
import constants as c

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_BAR, c.SCREEN_HEIGHT))

pg.display.set_caption("Tower Defense")

#LOAD IMAGES

map_image = pg.image.load('assets/images/levels/map.png').convert_alpha()

overlay_map_image = pg.image.load('assets/images/levels/mapoverlay.png').convert_alpha()

#individual turret image for mouse

cursor_turret = pg.image.load('assets/images/towers/frog.png').convert_alpha()

enemy_image = pg.image.load('assets/images/enemies/fly.png').convert_alpha()

enemy_image = pg.transform.scale(enemy_image, (80,80))

cursor_turret = pg.transform.scale(cursor_turret, (80,80))

map_image = pg.transform.scale(map_image, (880,880))

overlay_map_image = pg.transform.scale(overlay_map_image, (880,880))



def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    if (mouse_tile_x + 1, mouse_tile_y + 1) not in c.PATH_TILES and (mouse_tile_x + 1, mouse_tile_y + 1) not in c.OBSTACLE_TILES:
        #check if turret is already there:
        space_is_free = True
        for turret in turret_group:
            if  (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free:
            new_turret = Turret(cursor_turret, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

#CREATE WORLD
world = World(map_image)

overlay = World(overlay_map_image)

#CREATE GROUPS

enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

waypoints = [
    (680,0),
    (680,100),
    (460,100),
    (460,180),
    (120,180),
    (120,420),
    (360,420),
    (360,360),
    (600,360),
    (600, 680),
    (520, 680),
    (520, 760),
    (760, 760),
    (760, 600),
    (920, 600)
]

enemy = Enemy(waypoints, enemy_image)

enemy_group.add(enemy)

run = True

while run:

    clock.tick(c.FPS)

    screen.fill("grey")

    #draw level

    world.draw(screen)
    #draw waypoints for debugging
    # pg.draw.lines(screen, "black", False, waypoints)
    enemy_group.update()
    enemy_group.draw(screen)
    turret_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check if mouse on game are
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                create_turret(mouse_pos)

    overlay.draw(screen)
    pg.display.flip()

pg.quit()
