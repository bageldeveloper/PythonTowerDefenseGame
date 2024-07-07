import pygame as pg
from enemy import Enemy
from world import World
from turret import Turret
import constants as c
from button import Button
import turret_data as t
from pygame import mixer

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_BAR, c.SCREEN_HEIGHT))

pg.display.set_caption("Tower Defense")

#game variables
game_over = False
game_outcome = 0#-1 is loss, 1 is win
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None

#load music

# Starting the mixer 
mixer.init(909099) 
  
# Loading the song 
mixer.music.load("assets/audio/music/frogsong1.wav") 
song = 1  
# Setting the volume 
mixer.music.set_volume(0.7) 
  
# Start playing the song 
mixer.music.play() 

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
    turret_sheet = pg.transform.scale(turret_sheet, (240, 80))
    turret_spritesheets.append(turret_sheet)

enemy_images = {
    "fly": pg.transform.scale(pg.image.load('assets/images/enemies/flysheet.png').convert_alpha(), (480,80)),
    "ant": pg.transform.scale(pg.image.load('assets/images/enemies/fly.png').convert_alpha(), (80, 80)),
    "mosquito": pg.transform.scale(pg.image.load('assets/images/enemies/fly.png').convert_alpha(), (80, 80)),
    "cockroach": pg.transform.scale(pg.image.load('assets/images/enemies/fly.png').convert_alpha(), (80, 80)),
    
}



cursor_turret = pg.transform.scale(cursor_turret, (80,80))



map_image = pg.transform.scale(map_image, (880,880))

overlay_map_image = pg.transform.scale(overlay_map_image, (880,880))



ui_background_image = pg.transform.scale(ui_background_image, (440,880))


#BUTTONS YIPPEE

buy_turret_image = pg.image.load('assets/images/UI/frog_buy.png').convert_alpha()
cancel_image = pg.image.load('assets/images/UI/cancel.png').convert_alpha()
upgrade_image = pg.image.load('assets/images/UI/upgrade.png').convert_alpha()
begin_image = pg.image.load('assets/images/UI/begin.png').convert_alpha()
restart_image = pg.image.load('assets/images/UI/restart.png').convert_alpha()
win_image = pg.image.load('assets/images/UI/resart_win.png').convert_alpha()
fast_image = pg.image.load('assets/images/UI/fast_forward.png').convert_alpha()

buy_turret_image = pg.transform.scale(buy_turret_image, (150,150))

cancel_image = pg.transform.scale(cancel_image, (240,80))


upgrade_image = pg.transform.scale(upgrade_image, (240,80))
begin_image = pg.transform.scale(begin_image, (240,80))
restart_image = pg.transform.scale(restart_image, (150,50))
win_image = pg.transform.scale(win_image, (150,50))
fast_image = pg.transform.scale(fast_image, (100,100))

#load fonts for text
text_font = pg.font.SysFont("Consolas", 24, bold = True)
big_font = pg.font.SysFont("Consolas", 36)

#function for outputting text on screen

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def create_turret(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    if (mouse_tile_x + 1, mouse_tile_y + 1) not in c.PATH_TILES and (mouse_tile_x + 1, mouse_tile_y + 1) not in c.OBSTACLE_TILES:
        #check if turret is already there:
        space_is_free = True
        for turret in turret_group:
            if  (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
                upgrade_sound = pg.mixer.Sound("assets/audio/sfx/invalid.wav")
                pg.mixer.Sound.play(upgrade_sound)
        if space_is_free:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y, screen)
            turret_group.add(new_turret)
            upgrade_sound = pg.mixer.Sound("assets/audio/sfx/build.wav")
            pg.mixer.Sound.play(upgrade_sound)
            world.money -= c.BUY_COST
    else:
        upgrade_sound = pg.mixer.Sound("assets/audio/sfx/invalid.wav")
        pg.mixer.Sound.play(upgrade_sound)

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

def display_data():
    #draw panel

    draw_text(str(world.health), text_font, "white", c.SCREEN_WIDTH+ 120, 25)
    draw_text(str(world.level), text_font, "white", c.SCREEN_WIDTH + 240, 25)
    draw_text(str(world.money), text_font, "white", c.SCREEN_WIDTH + 370, 25)

def display_turret():
    cursor_rect = cursor_turret.get_rect()
    cursor_pos = pg.mouse.get_pos()
    cursor_rect.center = cursor_pos

    mouse_tile_x = cursor_pos[0] // c.TILE_SIZE
    mouse_tile_y = cursor_pos[1] // c.TILE_SIZE
    
    if cursor_pos[0] < c.SCREEN_WIDTH:
        if (mouse_tile_x + 1, mouse_tile_y + 1) not in c.PATH_TILES and (mouse_tile_x + 1, mouse_tile_y + 1) not in c.OBSTACLE_TILES and world.money >= c.BUY_COST:
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
world.process_enemies()




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



#create buttons
turret_button = Button(c.SCREEN_WIDTH + 45, 250, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 180, 670, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 180, 775, upgrade_image, True)
begin_button = Button(c.SCREEN_WIDTH + 180, 775, begin_image, True)
restart_button = Button(360, 440, restart_image, True)
win_button = Button(360, 440, win_image, True)
fast_button = Button(c.SCREEN_WIDTH + 45, 760, fast_image, False)
run = True

while run:

    if not mixer.music.get_busy():

        if song == 1:
            song = 2
            mixer.music.load("assets/audio/music/frogsong2.wav") 
            mixer.music.play()
        else:
            song = 1
            mixer.music.load("assets/audio/music/frogsong1.wav") 
            mixer.music.play()

    clock.tick(c.FPS)


    screen.fill("grey")

    ####################################
    # DRAW WORLD
    ##################################

    world.draw(screen)

    ####################################
    # UPDATING SECTION
    ##################################

    if game_over == False:
        if world.health <= 0:
            game_over = True
            game_outcome = -1
        #check if player won
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1 #win!!!!!!!


        enemy_group.update(world)
        turret_group.update(enemy_group, world)





    #highlight selected turret
        if selected_turret:
            selected_turret.selected = True


    ####################################
    # DRAW SECTION
    ##################################

    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)
    world.game_speed = 1

    if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN and level_started:
        if world.spawned_enemies < len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = Enemy(enemy_type, waypoints, enemy_images, screen)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pg.time.get_ticks()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # mouse click
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            # check if mouse on game are
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                    else:
                        upgrade_sound = pg.mixer.Sound("assets/audio/sfx/notenoughmoney.wav")
                        pg.mixer.Sound.play(upgrade_sound)

                else:
                    selected_turret = select_turret(mouse_pos)
    #check if level has been started or not
    if game_over == False:
        #spawn enemies


        if world.check_level_complete():
            world.money += c.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()
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
        if level_started == False:
            if begin_button.draw(screen):
                level_started = True
        if fast_button.draw(screen):
            world.game_speed = 2
        draw_text(str(t.FROG_COST), text_font, "white", c.SCREEN_WIDTH + 103, 365)
    else:
        #if can be upgraded show button
        if selected_turret.upgrade_level < c.TURRET_LEVELS:
            if upgrade_button.draw(screen):
                if world.money >= t.TURRET_DATA[selected_turret.upgrade_level].get("cost"):
                    upgrade_sound = mixer.Sound("assets/audio/sfx/upgrade.wav")
                    mixer.Sound.play(upgrade_sound)
                    selected_turret.upgrade()
                    world.money -=  t.TURRET_DATA[selected_turret.upgrade_level-1].get("cost")
   
    #display text
    display_data()


    if game_over:
        if game_outcome == 1:
            shape_surf = pg.Surface(pg.Rect((0, 0, 880, 880)).size, pg.SRCALPHA)
            pg.draw.rect(shape_surf, (0, 50, 0, 120), shape_surf.get_rect(), )
            screen.blit(shape_surf, (0, 0, 880, 880))

            shape_surf = pg.Surface(pg.Rect((240,340,400,200)).size, pg.SRCALPHA)
            pg.draw.rect(shape_surf, (0,255, 0, 120), shape_surf.get_rect(), border_radius = 30)
            screen.blit(shape_surf, (240,340,400,200))

            # pg.draw.rect(screen, "#ea6262", (240,340,400,200), border_radius = 30)

            draw_text("YOU WIN", big_font, "#ffffff", 350, 380)
            if win_button.draw(screen):
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pg.time.get_ticks()
                world = World(map_image)
                world.process_enemies()
                # clear enemies and turrets
                enemy_group.empty()
                turret_group.empty()
        else:
            shape_surf = pg.Surface(pg.Rect((0, 0, 880, 880)).size, pg.SRCALPHA)
            pg.draw.rect(shape_surf, (50, 0, 0, 120), shape_surf.get_rect(), )
            screen.blit(shape_surf, (0, 0, 880, 880))

            shape_surf = pg.Surface(pg.Rect((240, 340, 400, 200)).size, pg.SRCALPHA)
            pg.draw.rect(shape_surf, (255, 0, 0, 120), shape_surf.get_rect(), border_radius=30)
            screen.blit(shape_surf, (240, 340, 400, 200))

            # pg.draw.rect(screen, "#ea6262", (240,340,400,200), border_radius = 30)

            draw_text("GAME OVER", big_font, "#ffffff", 340, 380)
            if restart_button.draw(screen):
                game_over = False
                level_started = False
                placing_turrets = False
                selected_turret = None
                last_enemy_spawn = pg.time.get_ticks()
                world = World(map_image)
                world.process_enemies()
                # clear enemies and turrets
                enemy_group.empty()
                turret_group.empty()


    ####################################
    # SCREEN DISPLAY SECTION
    ##################################
    pg.display.flip()

pg.quit()
