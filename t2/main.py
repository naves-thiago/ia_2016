from map_loader import MapLoader
from gui import Gui
from prolog import PrologActor
from a_star import A_star

# Possiveis acoes:
# "T" - Atirar
# "R" - Rodar para a direita
# "A" - Andar pra frente
# "P" - Pegar ouro / powerup
# "S" - Ir para a saida
# "D" - Ir para uma posicao desconhecida

navegando = False   # Se true, estamos seguindo o caminho abaixo
caminho = []        # Caminho gerado pelo A*
passos_caminho = [] # Sequencia de movimentos para seguir o caminho
prox_passo = 0      # Proximo indice do passos_caminho
prox_caminho = 0    # Proximo indice do caminho

fim_nav = False
# Chamada do main loop para atualizar o agente e a tela
def update_map():
    global navegando, prox_passo, prox_caminho, caminho, passos_caminho, fim_nav
    #pl.atualiza()
    mapa_ator = pl.mapa
    gui.set_map_actor(mapa_ator)
    gui.set_status("Pontos: %d   Vida: %d" % (pl.pontos, pl.vida))

    #### TESTE
    if navegando and not fim_nav:
        if prox_passo == len(passos_caminho):
            fim_nav = True
            gui.set_path(None, 0)
            return

        if passos_caminho[prox_passo] == "A":
            prox_caminho += 1
            gui.set_path(caminho, prox_caminho)
            pl.andar_frente()
        else:
            pl.rodar()

        prox_passo += 1

    if not navegando and not fim_nav:
        navegando = True
        find_path(pl.mapa, pl.mapa[11][0], "U", pl.mapa[5][5])
        gui.set_path(caminho, 0)
    #######

    gui.set_actor_position(pl.pos, pl.dir)

def find_path(mapa, ini, dir_ini, fim):
    global caminho, passos_caminho
    a = A_star(mapa, ini, dir_ini, fim)
    a.run()

    seq, pos = path_to_move_sequence(fim)

    for p in pos:
        print(str(p))

    caminho = pos
    passos_caminho = seq

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

    return res, seq

# Ponto de entrada do programa
map_full = MapLoader("mapa.txt").mapa
pl = PrologActor("teste.pl")
gui = Gui(update_map)
gui.set_map_full(map_full)
gui.start_draw_loop()
