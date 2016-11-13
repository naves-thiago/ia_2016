import sys

class No:
    ''' Representa uma posicao para a qual podemos andar no mapa '''
    def __init__(self, x, y, tipo, custo=1, anterior=None, custo_acumulado=None):
        self.pos = (x,y)         # Posicao (x,y) no mapa
        self.tipo = tipo         # Tipo de No (para podermos representar na tela)
        self.anterior = anterior # De onde viemos
        self.custo = custo       # Custo de passar por esse No
        self.custo_acumulado = custo_acumulado # Custo acumulado da origem ate esse No

    def __str__(self):
        ''' Retorna uma string que representa esse no.
            nesse caso o par (x,y) da posicao '''
        return str(self.pos)

    def __lt__(self, other):
        ''' Permite comparar 2 Nos. (python 3)
            Compara os custos (eu sou menor que other?) '''
        if isinstance(other, No):
            return self.custo < other.custo
        else:
            return False

class MapLoader:
    def __init__(self, arquivo):
        ''' Carrega um mapa do arquivo '''
        self.max_x    = -1 # Posicao do ultimo char valido em cada linha do mapa
        self.max_y    = -1 # Numero de linhas -1 do mapa

        mapa_s = None  # Mapa versao string, lido do arquivo
        self.mapa = [] # Mapa de No

        # Suporte ao python 2 e 3
        if sys.version_info[0] < 3:
            mf = file(arquivo)
        else:
            mf = open(arquivo)

        mapa_s = mf.readlines()
        mf.close()
        self.max_x = len(mapa_s[0])-3 # Remove \r\n
        self.max_y = len(mapa_s)-1

        # Cria nos para as posicoes livres do mapa
        for y in range(self.max_y+1):
            linha = []
            self.mapa.append(linha)
            for x in range(self.max_x+1):
                linha.append(No(x, y, mapa_s[y][x]))


