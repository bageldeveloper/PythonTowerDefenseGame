import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
import constants as c
from button import Button
pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_BAR, c.SCREEN_HEIGHT))

pg.display.set_caption("Tower Defense")

#game variables
placing_turrets = False
selected_turret = None

#LOAD IMAGES

map_image = pg.image.load('assets/images/levels/map.png').convert_alpha()

overlay_map_image = pg.image.load('assets/images/levels/mapoverlay.png').convert_alpha()
ui_background_image = pg.image.load('assets/images/UI/UI_background.png').convert_alpha()

#individual turret image for mouse

cursor_turret = pg.image.load('assets/images/towers/frog.png').convert_alpha()

#turretspritesheets
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS+1):
    turret_sheet = pg.image.load(f'assets/images/towers/frogspritesheet_{x}.png').convert_alpha()

enemy_image = pg.image.load('assets/images/enemies/fly.png').convert_alpha()

enemy_image = pg.transform.scale(enemy_image, (80,80))

cursor_turret = pg.transform.scale(cursor_turret, (80,80))

turret_sheet = pg.transform.scale(turret_sheet, (240,80))

map_image = pg.transform.scale(map_image, (880,880))

overlay_map_image = pg.transform.scale(overlay_map_image, (880,880))



ui_background_image = pg.transform.scale(ui_background_image, (440,880))


#BUTTONS YIPPEE

buy_turret_image = pg.image.load('assets/images/UI/buyturret.png').convert_alpha()
cancel_image = pg.image.load('assets/images/UI/cancel.png').convert_alpha()
upgrade_image = pg.image.load('assets/images/UI/upgrade.png').convert_alpha()

buy_turret_image = pg.transform.scale(buy_turret_image, (150,50))

cancel_image = pg.transform.scale(cancel_image, (150,50))


upgrade_image = pg.transform.scale(upgrade_image, (150,50))






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
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, screen)
            turret_group.add(new_turret)

def select_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
            if  (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                return turret
        #check if turret is already there:

def clear_selection():
    for turret in turret_group:
        turret.selected = False
def display_turret():
    cursor_rect = cursor_turret.get_rect()
    cursor_pos = pg.mouse.get_pos()
    cursor_rect.center = cursor_pos

    mouse_tile_x = cursor_pos[0] // c.TILE_SIZE
    mouse_tile_y = cursor_pos[1] // c.TILE_SIZE
    
    if cursor_pos[0] < c.SCREEN_WIDTH:
        if (mouse_tile_x + 1, mouse_tile_y + 1) not in c.PATH_TILES and (mouse_tile_x + 1, mouse_tile_y + 1) not in c.OBSTACLE_TILES:
            #check if turret is already there:
            space_is_free = True
            for turret in turret_group:
                if  (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                    space_is_free = False
            if space_is_free:
                draw_pos = ((mouse_tile_x) * c.TILE_SIZE,(mouse_tile_y) * c.TILE_SIZE)
                opaque_cursor_turret = cursor_turret.copy()
                opaque_cursor_turret.fill((255, 255, 255, 128), None, pg.BLEND_RGBA_MULT)
                screen.blit(opaque_cursor_turret, draw_pos)
                
        else:
            draw_pos = ((mouse_tile_x) * c.TILE_SIZE,(mouse_tile_y) * c.TILE_SIZE)
            opaque_cursor_turret = cursor_turret.copy()
            opaque_cursor_turret.fill((255, 50, 50, 128), None, pg.BLEND_RGBA_MULT)
            screen.blit(opaque_cursor_turret, draw_pos)


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

#create buttons
turret_button = Button(c.SCREEN_WIDTH + 70, 30, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 70, 30, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 70, 30, upgrade_image, True)


run = True

while run:

    clock.tick(c.FPS)


    screen.fill("grey")

    ####################################
    # DRAW WORLD
    ##################################

    world.draw(screen)

    ####################################
    # UPDATING SECTION
    ##################################

    turret_group.update(enemy_group)

    enemy_group.update()

    #highlight selected turret
    if selected_turret:
        selected_turret.selected = True

    ####################################
    # DRAW SECTION
    ##################################

    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        #mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            #check if mouse on game are
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    ####################################
    # DRAW OVERLAY SECTION
    ##################################

    overlay.draw(screen)

    ####################################
    # DRAW UI SECTION
    ##################################

    screen.blit(ui_background_image, (880,0))

    if selected_turret == None:

        if turret_button.draw(screen) and placing_turrets == False:
            placing_turrets = True

        if placing_turrets:
            display_turret()
            if cancel_button.draw(screen):
                placing_turrets = False
        
    else:
        #if can be upgraded show button
        if selected_turret.upgrade_level < c.TURRET_LEVELS:
            if upgrade_button.draw(screen):
                selected_turret.upgrade()


    ####################################
    # SCREEN DISPLAY SECTION
    ##################################
    pg.display.flip()

pg.quit()
