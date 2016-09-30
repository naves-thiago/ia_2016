import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((640,480),0,32)
FPS = 24
clock =pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.draw.circle(screen, (200,0,0), (10,10), 10)
    pygame.display.flip()
    clock.tick(FPS)

