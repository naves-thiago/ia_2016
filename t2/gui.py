import pygame
import sys
from map_loader import *
from prolog import PrologActor

# Configs ##############

#sprite_size = (47, 47)
sprite_size = (50, 50)
map_size    = (12 * sprite_size[0], 12 * sprite_size[1])
maps_dist   = 30 # distance between the two maps
font_name   = "arial"
font_size   = 25
font_color  = (0, 150, 0)
text_offset = (10, 10)
bg_color    = (0, 0, 50)
FPS = 4

########################


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

class ColorRect:
    def __init__(self, color):
        self.color = color

    def draw(self, surface, pos):
        ''' Draw self on the surface at position pos (x,y) '''
        pygame.draw.rect(surface, self.color, pygame.Rect(pos, sprite_size))

class Gui:
    # Surface, Map
    def _draw_map(self, s, m):
        s.fill((0, 100, 20))
        for y in range(len(m)):
            for x in range(len(m[0])):
                if self.sprites.get(m[y][x].tipo):
                    self.sprites[m[y][x].tipo].draw(s, (x * sprite_size[0], y * sprite_size[1]));

    def __init__(self, new_frame_cb):
        self.frame_cb = new_frame_cb # Called before each frame to allow application to update the actor / map
        pygame.init()
        self.font = pygame.font.SysFont(font_name, font_size)
        window_size = (2 * map_size[0] + maps_dist, map_size[1] + text_offset[1] + self.font.get_height() + 10)
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Respect my authoritah!!")

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
        sprite_unknown  = ColorRect(pygame.Color(0,0,0))

        self.sprites = {"D":sprite_enemy1, "d":sprite_enemy2,   "U":sprite_powerup,
                        "P":sprite_hole,   "T":sprite_teleport, "O":sprite_gold,
                        "?":sprite_unknown}

        self.directions = {"U":sprite_up, "D":sprite_down, "L":sprite_left, "R":sprite_right}

        self.s_map_full  = pygame.Surface(map_size, pygame.SRCALPHA, 32)
        self.s_map_actor = pygame.Surface(map_size, pygame.SRCALPHA, 32)

        self.set_actor_position((0, 11), "U")


    def set_actor_position(self, pos, direction):
        ''' Updates both maps with a new actor position and direction. '''
        full_map_pos = (map_size[0] + maps_dist, 0)
        self.screen.blit(self.s_map_full, full_map_pos)
        self.screen.blit(self.s_map_actor, (0, 0))
        self.actor_pos = pos
        self.actor_dir = direction

    def set_map_full(self, m):
        ''' Updates the full map. '''
        self.map_full = m

    def set_map_actor(self, m):
        ''' Updates the actor map. '''
        self.map_actor = m

    def _draw_map_full(self):
        ''' Draws a new version of the full map. '''
        full_map_pos = (map_size[0] + maps_dist, 0)
        self._draw_map(self.s_map_full, self.map_full)
        self.screen.blit(self.s_map_full, full_map_pos)

    def _draw_map_actor(self):
        ''' Draws a new version of the actor map. '''
        self._draw_map(self.s_map_actor, self.map_actor)
        self.screen.blit(self.s_map_actor, (0,0))

    def _draw_actor(self):
        ''' Draws the actor on both maps. '''
        sprite = self.directions[self.actor_dir]
        act_offset = (sprite_size[0] * self.actor_pos[0], sprite_size[1] * self.actor_pos[1])

        full_map_pos = (map_size[0] + maps_dist, 0)
        full_act_pos = (full_map_pos[0] + act_offset[0], full_map_pos[1] + act_offset[1])

        sprite.draw(self.screen, full_act_pos)  # Full Map
        sprite.draw(self.screen, act_offset)    # Actor map

    def _draw_text(self):
        ren  = self.font.render(self.status_text, True, font_color)
        pos  = (text_offset[0], text_offset[1] + map_size[1])
        self.screen.blit(ren, pos)

    def set_status(self, txt):
        ''' Sets the status text. '''
        self.status_text = txt

    def start_draw_loop(self):
        ''' Main update / redraw loop. '''
        # Update the map / actor state
        self.frame_cb()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #sys.exit()
                    return

            self.screen.fill(bg_color)
            self.frame_cb()
            self._draw_map_actor()
            self._draw_map_full()
            self._draw_actor()
            self._draw_text()
            pygame.display.flip()
            clock.tick(FPS)


# Test code
## init(None)
## ml   = MapLoader("mapa.txt")
## mapa = ml.mapa
## _draw_map_full(mapa)
## 
## pl = PrologActor()
## pl.atualiza()
## mapa_t = pl.mapa
## #ml_t   = MapLoader("mapa_teste.txt")
## #mapa_t = ml_t.mapa
## _draw_map_actor(mapa_t)
## 
## set_actor_position((0, 11), "U")
## _draw_actor()
## 
## pygame.display.flip()
## #####
## 
## while True:
##     for event in pygame.event.get():
##         if event.type == pygame.QUIT:
##             pygame.quit()
##             sys.exit()
## 
## 
