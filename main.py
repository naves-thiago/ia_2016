from a_star import *
from map_loader import *
from map_display import *

# Caracteres usados
floresta  = "D"
inicio    = "I"
fim       = "F"
galho     = "G"
lobo      = "C"
vazio     = "."
solucao   = "S"
candidato = "A"
testado   = "T"

# Core de cada tipo de caminho / No
cores = {floresta:(0, 155, 0), galho:(140, 95, 0), vazio:(252, 217, 141), inicio:(252, 217, 141), fim:(252, 217, 141), lobo:(252, 252, 0), solucao:(220, 0, 0), candidato:(158, 195, 255), testado:(142, 0, 150)}

def custoCB(no):
    ''' Callback chamada pelo A* para obter o custo de um No
    com custo desconhecido (o lobo) '''
    return 0 # Ainda nao temos os custos. Por agora retorna 0

def gera_solucao(no):
    res = []
    atual = no
    while atual != None:
        res.append(atual)
        atual = atual.anterior

    res.reverse()
    return res

class MapState:
    DONE     = 1
    STEPS    = 2
    SOLUTION = 3

def mix_color(a, b):
    prop = 0.8 # a

    return (prop * a[0] + (1-prop)*b[0],
            prop * a[1] + (1-prop)*b[1],
            prop * a[2] + (1-prop)*b[2])


mapa_cor = None
steps = []
steps_index = 0
sol = None
sol_index = 0
map_state = MapState.STEPS
old_pos = None
old_color = None

def update_map_steps():
    global steps, steps_index, old_pos, old_color, mapa_cor
    if steps_index < len(steps):
        if steps[steps_index]: # Make sure this is not None
            v, c = steps[steps_index] # Visited, candidates

            # Paint the last tested position as a candidate
            if old_pos:
                mapa_cor[old_pos[1]][old_pos[0]] = mix_color(old_color, cores[candidato])

            old_pos = v.pos
            old_color = mapa_cor[v.pos[1]][v.pos[0]]

            mapa_cor[v.pos[1]][v.pos[0]] = mix_color(old_color, cores[testado])
            for ci in c:
                mc = mapa_cor[ci.pos[1]][ci.pos[0]]
                mapa_cor[ci.pos[1]][ci.pos[0]] = mix_color(mc, cores[candidato])

            steps_index += 1
        else:
            return True
    else:
        return True

    return False


def update_map_solution():
    global sol, sol_index, mapa_cor
    if sol_index < len(sol):
        n = sol[sol_index]
        mapa_cor[n.pos[1]][n.pos[0]] = cores[solucao]
        sol_index += 1
    else:
        return True

    return False

def get_map():
    global map_state, mapa_cor

    if map_state == MapState.SOLUTION:
        if update_map_solution():
            map_state = MapState.DONE

    elif map_state == MapState.STEPS:
        if update_map_steps():
            map_state = MapState.SOLUTION

    return mapa_cor

def main():
    global mapa_cor, steps, sol
    mapLoader = MapLoader("mapa_trabalho.txt")
    print("Inicio: "+str(mapLoader.p_inicio))
    print("Fim: "+str(mapLoader.p_fim))
    mapa = mapLoader.mapa
    busca = A_star(mapa, mapLoader.p_inicio, mapLoader.p_fim, custoCB)

    i = busca.step()
    while i != None:
        i = busca.step()
        steps.append(i)

    sol = gera_solucao(busca.no_fim)

    mapa_cor = converteMapa(mapa, cores)
    mostraMapa(get_map)

main()
