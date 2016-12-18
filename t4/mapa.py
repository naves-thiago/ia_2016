class No:
    ''' Representa uma posicao para a qual podemos andar no mapa '''
    def __init__(self, x, y, tipo, custo=1):
        self.pos = (x,y)         # Posicao (x,y) no mapa
        self.tipo = tipo         # Tipo de No (para podermos representar na tela)

        # Variaveis de estado para busca
        self.anterior = None        # De onde viemos
        self.custo = custo          # Custo de passar por esse No
        self.custo_acumulado = None # Custo acumulado da origem ate esse No
        self.direcao = None         # Direcao em que entramos nesse No
        self.prioridade = 9999999   # Define a ordem dos Nos na heap

    def __str__(self):
        ''' Retorna uma string que representa esse no.
            nesse caso o par (x,y) da posicao '''
        return str(self.pos)

    def __lt__(self, other):
        ''' Permite comparar 2 Nos. (python 3)
            Compara os custos (eu sou menor que other?) '''
        if isinstance(other, No):
            return self.prioridade < other.prioridade
        else:
            return False

class Mapa:
    size = (59, 34)
    def __init__(self):
        ''' Cria um mapa vazio '''
        self.mapa = []
        for y in range(Mapa.size[1]):
            l = [No(x, y, "?") for x in range(Mapa.size[0])]
            self.mapa.append(l)

        self.ouros = []
        self.power_ups = []

    def get(self, x, y):
        ''' Retorna o No na posicao (x, y) ou None se a posicao for invalida '''
        if x >= 0 and x < Mapa.size[0] and y >= 0 and y < Mapa.size[1]:
            return self.mapa[y][x]
        else:
            return None

    def getManhattan2(self, x, y):
        ''' Retorna os Nos com distancia manhattan <= 2 de (x, y) '''
        l = [(x-2, y), (x+2, y), (x, y-2), (x, y+2),
             (x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1),
             (x-1, y), (x+1, y), (x, y-1), (x, y+1)]

        res = []
        for x, y in l:
            n = self.get(x,y)
            if n:
                res.append(n)

        return res
