from a_star import *
from map_loader import *
from map_display import *

# Caracteres usados
floresta = "D"
inicio   = "I"
fim      = "F"
galho    = "G"
lobo     = "C"
vazio    = "."
solucao  = "S"

# Core de cada tipo de caminho / No
cores = {floresta:(0, 155, 0), galho:(140, 95, 0), vazio:(252, 217, 141), inicio:(252, 217, 141), fim:(252, 217, 141), lobo:(252, 252, 0), solucao:(220, 0, 0)}

def custoCB(no):
    ''' Callback chamada pelo A* para obter o custo de um No
    com custo desconhecido (o lobo) '''
    return 0 # Ainda nao temos os custos. Por agora retorna 0

def solucao(no):
    atual = no
    while atual != None:
        atual.tipo = "S"
        atual = atual.anterior

def main():
    mapLoader = MapLoader("mapa_trabalho.txt")
    print("Inicio: "+str(mapLoader.p_inicio))
    print("Fim: "+str(mapLoader.p_fim))
    mapa = mapLoader.mapa
    busca = A_star(mapa, mapLoader.p_inicio, mapLoader.p_fim, custoCB)

    while busca.step() != None:
        pass

    solucao(busca.no_fim)
    mapa_cor = converteMapa(mapa, cores)
    mostraMapa(mapa_cor)

main()
