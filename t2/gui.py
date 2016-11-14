import pygame
import sys
from map_loader import *

# Configs ##############

#sprite_size = (47, 47)
sprite_size = (50, 50)
map_size    = (12 * sprite_size[0], 12 * sprite_size[1])
maps_dist   = 50 # distance between the two maps
window_size = (2 * map_size[0] + maps_dist, map_size[1])
FPS = 24

########################

frame_cb = None # Called before each frame to allow application to update the actor / map

class Sprite:
    def __init__(self, img_file, rect=None, scale=(1,1)):
        ''' Load an image file as an sprite. Optionally use only the area defined in rect and change scale. '''
        f_img = pygame.image.load(img_file)

        if rect != None:
            # Extract the part of the image defined by rect
            tmp = pygame.Surface(rect.size, f_img.get_flags(), f_img.get_bitsize())
            tmp.blit(f_img, (0,0), rect)
        else:
            # Use the whole image
            tmp = f_img

        # Scale the image if needed
        if tmp.get_rect().size == sprite_size and scale == (1,1):
            self.img = tmp
        else:
            size = (int(round(sprite_size[0] * scale[0])),      int(round(sprite_size[1] * scale[1])))
            pos  = (int(round((sprite_size[0] - size[0]) / 2)), int(round((sprite_size[1] - size[1]) / 2)))
            self.img = pygame.Surface(sprite_size, pygame.SRCALPHA, 32)
            self.img.blit(pygame.transform.smoothscale(tmp, size), pos)

    def draw(self, surface, pos):
        ''' Draw self on the surface at position pos (x,y) '''
        surface.blit(self.img, pos)

# Surface, Map
def _draw_map(s, m):
    s.fill((0, 100, 20))
    for y in range(len(m)):
        for x in range(len(m[0])):
            if sprites.get(m[y][x].tipo):
                sprites[m[y][x].tipo].draw(s, (x * sprite_size[0], y * sprite_size[1]));

def init(new_frame_cb):
    global screen, sprite_up, sprite_right, sprite_left, sprite_hole, sprite_enemy1
    global sprite_enemy2, sprite_gold, sprite_teleport, sprite_powerup, sprites
    global s_map_full, s_map_actor, directions, frame_cb

    frame_cb = new_frame_cb
    pygame.init()
    screen = pygame.display.set_mode(window_size)

    # Load sprites
    sprite_up       = Sprite("imagens/kenny.png", pygame.Rect(0, 0,   47, 47), (0.7, 0.7))
    sprite_right    = Sprite("imagens/kenny.png", pygame.Rect(0, 47,  47, 47), (0.7, 0.7))
    sprite_down     = Sprite("imagens/kenny.png", pygame.Rect(0, 94,  47, 47), (0.7, 0.7))
    sprite_left     = Sprite("imagens/kenny.png", pygame.Rect(0, 141, 47, 47), (0.7, 0.7))

    sprite_hole     = Sprite("imagens/hole.png", None, (0.7, 0.7))
    sprite_enemy1   = Sprite("imagens/satan.png")
    sprite_enemy2   = Sprite("imagens/saddam-hussein.png")
    sprite_gold     = Sprite("imagens/coins_1.png", None, (0.6, 0.6))
    sprite_powerup  = Sprite("imagens/chinpokomon.png", None, (0.6, 0.6))
    sprite_teleport = Sprite("imagens/teleport.png")

    sprites = {"D":sprite_enemy1, "d":sprite_enemy2,   "U":sprite_powerup,
               "P":sprite_hole,   "T":sprite_teleport, "O":sprite_gold}

    directions = {"U":sprite_up, "D":sprite_down, "L":sprite_left, "R":sprite_right}

    s_map_full  = pygame.Surface(map_size, pygame.SRCALPHA, 32)
    s_map_actor = pygame.Surface(map_size, pygame.SRCALPHA, 32)

def _draw_map_full(m):
    ''' Draws a new version of the full map. '''
    global s_map_full, screen
    _draw_map(s_map_full, m)
    screen.blit(s_map_full, (0,0))

def _draw_map_actor(m):
    ''' Draws a new version of the actor map. '''
    global s_map_actor, screen
    _draw_map(s_map_actor, m)
    screen.blit(s_map_actor, (0,0))

def set_actor_position(pos, direction):
    ''' Updates both maps with a new actor position and direction. '''
    global s_map_actor, s_map_full, actor_pos, actor_dir, screen
    f_map_pos = (map_size[0] + maps_dist, 0)
    screen.blit(s_map_full, f_map_pos)
    screen.blit(s_map_actor, (0, 0))
    actor_pos = pos
    actor_dir = direction

def _draw_actor():
    ''' Draws the actor on both maps. '''
    global screen, directions, actor_pos, actor_dir
    sprite = directions[actor_dir]
    act_offset = (sprite_size[0] * actor_pos[0], sprite_size[1] * actor_pos[1])

    f_map_pos = (map_size[0] + maps_dist, 0)
    f_act_pos = (f_map_pos[0] + act_offset[0], f_map_pos[1] + act_offset[1])

    sprite.draw(screen, f_act_pos)  # Full Map
    sprite.draw(screen, act_offset) # Actor map

# Test code
init(None)
ml   = MapLoader("mapa.txt")
mapa = ml.mapa
_draw_map_full(mapa)

ml_t   = MapLoader("mapa_teste.txt")
mapa_t = ml_t.mapa
_draw_map_actor(mapa_t)

#_draw_map(s_map_full, mapa)
#screen.blit(s_map_full, (0,0))

set_actor_position((0, 11), "U")
_draw_actor()

# s.fill((0, 100, 20))
# sprite_up.draw(s, (10, 10))
# sprite_right.draw(s, (80, 10))
# sprite_down.draw(s, (150, 10))
# sprite_left.draw(s, (230, 10))
# sprite_hole.draw(s, (300, 10))
# sprite_enemy1.draw(s, (10, 80))
# sprite_enemy2.draw(s, (80, 80))
# sprite_gold.draw(s, (150, 80))
pygame.display.flip()
#####

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


