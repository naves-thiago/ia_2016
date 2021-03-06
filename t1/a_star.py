import heapq
from map_loader import No

class A_star:
    def _vizinhos(self, no):
        ''' Retorna a lista de vizinhos do no '''
        res = []
        x, y = no.pos
        if x > 0:
            res.append(self.mapa[y][x-1])

        if x < self.max_x:
            res.append(self.mapa[y][x+1])

        if y > 0:
            res.append(self.mapa[y-1][x])

        if y < self.max_y:
            res.append(self.mapa[y+1][x])

        return res

    def _distancia(self, a, b):
        ''' Calcula a distancia manhattan entre a e b.
        a e b sao nos '''
        #return 0
        return abs(b.pos[0] - a.pos[0]) + abs(b.pos[1] - a.pos[1])

    def __init__(self, mapa, pos_ini, pos_fim, custoCB=None):
        # Guarda o mapa
        self.mapa = mapa
        self.max_x = len(mapa[0])-1
        self.max_y = len(mapa)-1
        self.pos_fim = pos_fim

        # Callback para obter o custo de um no com custo None
        self.custoCB = custoCB

        # Guarda os nos inicial e final
        self.no_ini = mapa[pos_ini[1]][pos_ini[0]]
        self.no_fim = mapa[pos_fim[1]][pos_fim[0]]

        # Insere a posicao inicial
        self.fronteira = [(0, self.no_ini)]
        self.no_ini.custo_acumulado = 0

    # Retorna True se terminou a busca
    def step(self):
        atual = heapq.heappop(self.fronteira)[1] # elem da heap = (custo, No)

        if atual == self.no_fim:
            return None

        viz = self._vizinhos(atual)
        for v in viz:
            if v.custo == None:
                if self.custoCB != None:
                    v.custo = self.custoCB(v)
                else:
                    raise Exception("Falha ao obter o custo para o No "+str(v))

            custo = atual.custo_acumulado + v.custo
            if v.custo_acumulado == None or v.custo_acumulado > custo:
                v.custo_acumulado = custo
                prioridade = custo + self._distancia(self.no_fim, v)
                heapq.heappush(self.fronteira, (prioridade, v))
                v.anterior = atual

        return (atual, viz)
