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
# "I" - Subir

navegando = False   # Se true, estamos seguindo o caminho abaixo
caminho = []        # Caminho gerado pelo A*
acoes_caminho = []  # Sequencia de movimentos para seguir o caminho
prox_acao = 0       # Proximo indice do acoes_caminho
prox_caminho = 0    # Proximo indice do caminho
saiu = False        # Saiu da caverna. Para de fazer update()
desistiu = False    # Indo para a saida sem os 3 ouros

# Chamada do main loop para atualizar o agente e a tela
def update():
    global navegando, prox_acao, prox_caminho, caminho, acoes_caminho, fim_nav, saiu

    if saiu:
        return

    if navegando:
        navigation_step()
        pl.observar()
    else:
        if desistiu:
            subir()
            return

        pl.observar()
        a = pl.melhor_acao()
        {"T":pl.atirar, "R":pl.rodar, "A":pl.andar_frente, "P":pl.pegar_item, "S":goto_exit, "D":goto_unvisited, "I":subir}[a]()

    gui.set_map_actor(mapa_ator)
    gui.set_status("Pontos: %d   Vida: %d   Ouros: %d   Balas: %d" % (pl.pontos, pl.vida, pl.ouros, pl.balas))
    gui.set_actor_position(pl.pos, pl.dir)

def subir():
    global saiu
    pl.sair()
    saiu = True

def goto_exit():
    ''' Navega para a saida. '''
    start_navigation(mapa_ator[11][0])

def goto_unvisited():
    ''' Navega para o No nao visitado mais proximo. '''
    global desistiu

    no = find_unvisited()
    # print("Goto: " + str(no))  #### DEBUG
    if not no:
        # Se nao consegue ir para mais nenhum lugar, vai pra saida
        goto_exit()
        desistiu = True
        return
    start_navigation(no)

def navigation_step():
    ''' Executa a proxima acao na navegacao. '''
    global navegando, prox_acao, acoes_caminho, caminho, prox_caminho

    if prox_acao == len(acoes_caminho) -1:
        navegando = False
        gui.set_path(None, 0)
        return

    if acoes_caminho[prox_acao] == "A":
        prox_caminho += 1
        gui.set_path(caminho, prox_caminho)
        pl.andar_frente()
    else:
        pl.rodar()

    prox_acao += 1


def start_navigation(dest):
    ''' Inicia a navegacao por um percurso gerado em uma busca A* da posicao atual ate dest. '''
    global navegando, prox_acao, prox_caminho, caminho, acoes_caminho
    navegando = True
    prox_acao = 0
    prox_caminho = 0
    find_path(mapa_ator, mapa_ator[pl.pos[1]][pl.pos[0]], pl.dir, dest)
    gui.set_path(caminho, 0)

def find_path(mapa, ini, dir_ini, fim):
    ''' Encontra um caminho de ini ate fim e atualiza as variaveis globais com o caminho encontrado. '''
    global caminho, acoes_caminho
    a = A_star(mapa, ini, dir_ini, fim)
    a.run()

    seq, pos = get_move_sequence(fim)

    caminho = pos
    acoes_caminho = seq

def find_unvisited():
    ''' Retorna o No nao visitado mais proximo. '''
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
    if len(candidatos) == 0:
        return None

    melhor = candidatos[0]
    for c in candidatos:
        if c.custo_acumulado < melhor.custo_acumulado:
            melhor = c

    return melhor

def get_move_sequence(dest):
    ''' Retorna a sequencia de acoes para chegar a dest e o caminho a percorrer. '''
    pos   = [] # Sequencia de posicoes
    steps = [] # Sequencia de acoes (vira, anda...)
    a = dest
    while a:
        pos.insert(0, a)
        if a == mapa_ator[pl.pos[1]][pl.pos[0]]:
            break
        a = a.anterior

    for i in range(len(pos)-1):
        # Roda o numero de vezes necessario
        steps.extend(A_star.rotacoes(pos[i], pos[i+1], pos[i].direcao) * ["R"])
        steps.append("A") # Anda pra frente

    return steps, pos

# Ponto de entrada do programa
map_full = MapLoader("mapa.txt").mapa
#pl = PrologActor("teste.pl")
pl = PrologActor("novo.pl")
mapa_ator = pl.mapa
gui = Gui(update)
gui.set_map_full(map_full)
gui.start_draw_loop()
