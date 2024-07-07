ROWS = 11
COLS = 11
TILE_SIZE = 80
SIDE_BAR = 440
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS

HEALTH = 10
MONEY = 300
BUY_COST = 100
UPGRADE_COST = 50
KILL_REWARD = 1
LEVEL_COMPLETE_REWARD = 100
#turret constants
ANIMATION_STEPS = 3
ANIMATION_DELAY = 100
TURRET_LEVELS = 4
DAMAGE = 5
#enemy constants
ENEMY_ANIMATION_STEPS = 6
ENEMY_ANIMATION_DELAY = 60
TOTAL_LEVELS = 4

FPS = 60

PATH_TILES = [
    (9, 1),
    (9, 2),
    (8, 2),
    (7, 2),
    (6, 2),
    (6, 3),
    (5, 3),
    (4, 3),
    (3, 3),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 6),
    (4, 6),
    (5, 6),
    (5, 5),
    (6, 5),
    (7, 5),
    (8, 5),
    (8, 6),
    (8, 7),
    (8, 8),
    (8, 9),
    (7, 9),
    (7, 10),
    (8, 10),
    (9, 10),
    (10, 10),
    (10, 9),
    (10, 8),
    (11, 8)
]
OBSTACLE_TILES = [
    (1, 11),
(2, 11),
(3, 11),
    (4,11),
(1, 10),
(2, 10),
(3, 10),
(4,10),
(1, 9),
(2, 9),
(3, 9),
(4, 9),
(5,9),
(1,8),
(2, 8),
(3, 8),
(4, 8),
(5,8),
(2,7),
(3,7),
(4,7),
(5,7),
(11, 2),
(9, 3),
(10, 3),
(11, 3),
(10, 4),
(11, 4),
]


#enemy constants
SPAWN_COOLDOWN =600
