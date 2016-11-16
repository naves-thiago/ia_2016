from map_loader import MapLoader
from gui import Gui
from prolog import PrologActor
from a_star import A_star

def update_map():
    pl.atualiza()
    mapa_ator = pl.mapa
    gui.set_map_actor(mapa_ator)

def find_unvisited():
    x, y = pl.pos
    no_ini = mapa_ator[y][x]
    a = A_star(mapa_ator, no_ini, pl.dir, None)
    a.run()

    # Encontra todos os nao visitados alcancaveis
    candidatos = []
    for y in mapa_ator:
        for x in y:
            if x.tipo == "?" and x.custo_acumulado != None:
                candidatos.append(x)

    # Econtra o No mais proximo entre os candidatos
    melhor = candidatos[0]
    for c in candidatos:
        if c.custo_acumulado < melhor.custo_acumulado:
            melhor = c

    return melhor


# Ponto de entrada do programa
map_full = MapLoader("mapa.txt").mapa
pl = PrologActor("teste.pl")
gui = Gui(update_map)
gui.set_map_full(map_full)
#gui.set_map_actor(map_full)
gui.start_draw_loop()
