import pygame
import sys

# Configs ##############

#sprite_size = (47, 47)
sprite_size = (60, 60)
FPS = 24

########################

# Sprites
class Sprite:
    def __init__(self, img_file, rect=None):
        ''' Load an image file as an sprite. Optionally use only the area defined in rect. '''
        f_img = pygame.image.load(img_file)
        self.img = pygame.Surface(sprite_size, pygame.SRCALPHA, 32)
        self.img.convert_alpha()

        if rect != None:
            # Extract the part of the image defined by rect
            tmp = pygame.Surface(rect.size, f_img.get_flags(), f_img.get_bitsize())
            tmp.blit(f_img, (0,0), rect)
        else:
            # Use the whole image
            tmp = f_img

        # Scale the image if needed
        if tmp.get_rect().size == sprite_size:
            self.img = tmp
        else:
            self.img = pygame.transform.smoothscale(tmp, sprite_size)

    def draw(self, surface, pos):
        ''' Draw self on the surface at position pos (x,y) '''
        surface.blit(self.img, pos)


pygame.init()
s = pygame.display.set_mode((640, 480))

# Load actor sprites
sprite_up     = Sprite("kenny.png", pygame.Rect(0, 0,   47, 47))
sprite_right  = Sprite("kenny.png", pygame.Rect(0, 47,  47, 47))
sprite_down   = Sprite("kenny.png", pygame.Rect(0, 94,  47, 47))
sprite_left   = Sprite("kenny.png", pygame.Rect(0, 141, 47, 47))

sprite_hole   = Sprite("hole.png")
sprite_enemy1 = Sprite("satan.png")
sprite_enemy2 = Sprite("saddam-hussein.png")

# Test code
s.fill((0, 100, 20))
sprite_up.draw(s, (10, 10))
sprite_right.draw(s, (80, 10))
sprite_down.draw(s, (150, 10))
sprite_left.draw(s, (230, 10))
sprite_hole.draw(s, (300, 10))
sprite_enemy1.draw(s, (10, 80))
sprite_enemy2.draw(s, (10, 150))
pygame.display.flip()
#####

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


