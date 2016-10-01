import sys
from a_star import *

# Caracteres usados
floresta = "D"
inicio   = "I"
fim      = "F"
galho    = "G"
lobo     = "C"
vazio    = "."
caminho  = "\x1b[41m \x1b[40m" # Colorido =)
#caminho  = "_" # Sem cores

# Custos dos caminhos
custos = {floresta:200, galho:5, vazio:1, inicio:0, fim:0, lobo:0}

max_x    = -1 # Posicao do ultimo char valido em cada linha do mapa
max_y    = -1 # Numero de linhas -1 do mapa
p_inicio = (-1,-1) # posicao de inicio (x,y)
p_fim    = (-1,-1) # posicao de termino (x,y)

mapa_s = None  # Mapa versao string, lido do arquivo
mapa = []      # Mapa de No
def carrega_mapa(arquivo):
    global mapa, mapa_s, max_x, max_y, p_inicio, p_fim
    mf = file(arquivo)
    mapa_s = mf.readlines()
    mf.close()
    max_x = len(mapa_s[0])-3 # Remove \r\n
    max_y = len(mapa_s)-1

    # Cria nos para as posicoes livres do mapa
    for y in range(max_y+1):
        linha = []
        mapa.append(linha)
        for x in range(max_x+1):
            linha.append(No(x, y, None, False, custos[mapa_s[y][x]]))

            if mapa_s[y][x] == inicio:
                p_inicio = (x,y)

            if mapa_s[y][x] == fim:
                p_fim = (x,y)

# Retorna a lista de nos que representam o caminho percorrido
def solucao(no):
    res = []
    atual = no
    while atual != None:
        res.append(atual)
        atual = atual.anterior

    return res

# Imprime o mapa original
def print_mapa():
    for l in mapa_s:
        sys.stdout.write(l)  # o mesmo que print, mas sem quebra de linha
    print("")

def print_solucao(sol):
    # Converte o mapa de string para vetor de char/strings
    mapa2 = []
    for l in mapa_s:
        mapa2.append([x for x in l])

    # Altera o novo mapa para marcar o caminho
    for n in sol:
        mapa2[n.pos[1]][n.pos[0]] = caminho

    # Converte de volta pra string para imprimir com a mesma cara
    for l in mapa2:
        tmp = ""
        for c in l:
            tmp += c
        sys.stdout.write(tmp)

    print("")

##### MAIN ######
carrega_mapa("mapa_trabalho.txt")
print("Inicio: "+str(p_inicio))
print("Fim: "+str(p_fim))

a = A_star(mapa, p_inicio, p_fim)

while a.step() != None:
    continue

sol = solucao(a.no_fim)
print_solucao(sol)

'''
for i in range(5):
    fim, viz = a.step()
    print(fim)
    print(str(fim)+" - "+str([str(x) for x in viz]))
sol = solucao(fim)
print_solucao(sol)
'''

'''
sol = bfs(p_inicio, p_fim)
print_mapa()
print("-------------------------------------\n")

'''

