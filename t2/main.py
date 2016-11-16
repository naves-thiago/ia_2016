from map_loader import MapLoader
from gui import Gui
from prolog import PrologActor
from a_star import A_star

def update_map():
    pl.atualiza()
    mapa_ator = pl.mapa
    gui.set_map_actor(mapa_ator)
    gui.set_status("Pontos: %d   Vida: %d" % (pl.pontos, pl.vida))

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

def path_to_move_sequence(dest):
    seq = [] # Sequencia de posicoes
    res = [] # Sequencia de passos (vira, anda...)
    a = dest
    while a:
        seq.insert(0, a)
        a = a.anterior

    for i in range(len(seq)-1):
        # Roda o numero de vezes necessario
        res.extend(A_star.rotacoes(seq[i], seq[i+1], seq[i].direcao) * ["R"])
        res.append("A") # Anda pra frente

    return res

# Ponto de entrada do programa
map_full = MapLoader("mapa.txt").mapa
pl = PrologActor("teste.pl")
gui = Gui(update_map)
gui.set_map_full(map_full)
gui.start_draw_loop()
