import sys
import pygame
import a_star

### Configs ###

FPS = 24
tamanho_sprite = (16, 16)

###############

def converteMapa(mapa, cores):
    ''' Converte uma matriz de No para uma matriz de cores (tuplas RGB) '''
    res = []
    for l in mapa:
        linha = []
        res.append(linha)
        for c in l:
            linha.append(cores[c.tipo])

    return res

def _desenhaMapa(screen, mapa):
    sz_x = tamanho_sprite[0]
    sz_y = tamanho_sprite[1]

    for y in range(len(mapa)):
        for x in range(len(mapa[y])):
            pygame.draw.rect(screen, mapa[y][x], pygame.Rect(x*sz_x, y*sz_y, sz_x, sz_y))

def mostraMapa(mapa):
    pygame.init()
    tamanho_tela = (tamanho_sprite[0]*len(mapa[0]), tamanho_sprite[1]*len(mapa))
    screen = pygame.display.set_mode(tamanho_tela,0,32)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        _desenhaMapa(screen, mapa)
        pygame.display.flip()
        clock.tick(FPS)

