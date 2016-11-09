import sys

# Caracteres usados
parede   = "X"
inicio   = "I"
fim      = "F"
vazio    = "."
caminho  = "\x1b[41m \x1b[40m" # Colorido =)
#caminho  = "_" # Sem cores

max_x    = -1 # Posicao do ultimo char valido em cada linha do mapa
max_y    = -1 # Numero de linhas -1 do mapa
p_inicio = (-1,-1) # posicao de inicio (x,y)
p_fim    = (-1,-1) # posicao de termino (x,y)

mapa_s = None  # Mapa versao string, lido do arquivo
mapa = {}      # Mapa esparso so com os caminhos livres
def carrega_mapa(arquivo):
	global mapa, mapa_s, max_x, max_y, p_inicio, p_fim
	mf = file(arquivo)
	mapa_s = mf.readlines()
	mf.close()
	max_x = len(mapa_s[0])-2
	max_y = len(mapa_s)-1

	# Cria nos para as posicoes livres do mapa
	for x in range(max_x):
		for y in range(max_y):
			if mapa_s[y][x] == vazio:
				mapa[(x,y)]=No(x, y, None, False)

			if mapa_s[y][x] == inicio:
				mapa[(x,y)]=No(x, y, None, False)
				p_inicio = (x,y)

			if mapa_s[y][x] == fim:
				mapa[(x,y)]=No(x, y, None, False)
				p_fim = (x,y)

# Representa uma posicao para a qual podemos andar no mapa
class No:
	pos = (-1, -1)   # Posicao (x,y) no mapa
	anterior = None  # De onde viemos
	visitado = False # Ja visitamos esse no?

	# Construtor do objeto no. Sobrescreve as variaveis acima
	def __init__(self, x, y, anterior=None, visitado=False):
		self.pos = (x,y)
		self.anterior = anterior
		self.visitado = visitado

	# Retorna uma string que representa esse no.
	# nesse caso o par (x,y) da posicao
	def __str__(self):
		return str(self.pos)

# Retorna um vetor com os possiveis passos a partir do no passado no parametro
# Tambem define o no passado como anterior desses nos, assim guardamos o caminho andado
def get_caminhos(no):
	x, y = no.pos
	res = []
	if x > 0:
		n = mapa.get((x-1, y))
		if n and not n.visitado:
			n.anterior = no
			res.append(n)

	if y > 0:
		n = mapa.get((x, y-1))
		if n and not n.visitado:
			n.anterior = no
			res.append(n)

	if x < max_x:
		n = mapa.get((x+1, y))
		if n and not n.visitado:
			n.anterior = no
			res.append(n)

	if y < max_y:
		n = mapa.get((x, y+1))
		if n and not n.visitado:
			n.anterior = no
			res.append(n)

	return res

# Faz a busca em largura do caminho
def bfs(pos_ini, pos_fim):
	a_visitar = [mapa[p_inicio]]

	while len(a_visitar) > 0:
		atual = a_visitar.pop(0)
		if atual.visitado:
			continue

		if atual.pos == pos_fim:
			return solucao(atual)

		atual.visitado = True
		a_visitar += get_caminhos(atual)

# Faz a busca em profundidade do caminho
def dfs(pos_ini, pos_fim):
	a_visitar = [mapa[p_inicio]]

	while len(a_visitar) > 0:
		atual = a_visitar.pop()
		if atual.visitado:
			continue

		if atual.pos == pos_fim:
			return solucao(atual)

		atual.visitado = True
		a_visitar += get_caminhos(atual)


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


##### MAIN ######
carrega_mapa("mapa1.txt")
print("Inicio: "+str(p_inicio))
print("Fim: "+str(p_fim))
sol = bfs(p_inicio, p_fim)
print_mapa()
print("-------------------------------------\n")

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

