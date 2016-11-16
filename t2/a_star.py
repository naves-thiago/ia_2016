import heapq
from map_loader import No

class A_star:
    def _vizinhos(self, no):
        ''' Retorna a lista de vizinhos do no '''
        res = []
        x, y = no.pos
        if x > 0 and self.mapa[y][x-1].tipo == ".":
            res.append(self.mapa[y][x-1])

        if x < self.max_x and self.mapa[y][x+1].tipo == ".":
            res.append(self.mapa[y][x+1])

        if y > 0 and self.mapa[y-1][x].tipo == ".":
            res.append(self.mapa[y-1][x])

        if y < self.max_y and self.mapa[y+1][x].tipo == ".":
            res.append(self.mapa[y+1][x])

        return res

    def _distancia(self, a, b):
        ''' Calcula a distancia manhattan entre a e b. a e b sao nos. '''
        if a == None or b == None:
            return 0
        return abs(b.pos[0] - a.pos[0]) + abs(b.pos[1] - a.pos[1])

    @staticmethod
    def direcao(orig, dest):
        ''' Retorna a direcao de movimento para ir de orig a dest. '''
        if dest.pos[1] < orig.pos[1]:
            d = "U"
        elif dest.pos[0] > orig.pos[0]:
            d = "R"
        elif dest.pos[1] > orig.pos[1]:
            d = "D"
        else:
            d = "L"

        return d

    _num_rotacao = {"U":1, "R":2, "D":3, "L":4}
    def _rotacoes(self, orig, dest, direcao):
        ''' Calcula quantas rotacoes fazer para ir de orig para dest.
            _rotacoes(orig, dest, direcao) -> numero de rotacoes. '''
        #      1
        #      ^
        #      |
        # 4 <--+--> 2
        #      |
        #     \/
        #      3
        #
        # Atribuindo um dos numeros acima a cada direcao, podemos
        # calcular o numero de rotacoes por (dest - orig + 4) % 4

        o = self._num_rotacao[direcao]
        d = self._num_rotacao[self.direcao(orig, dest)]

        return (d - o + 4) % 4

    def __init__(self, mapa, no_ini, dir_ini, no_fim):
        ''' Cria um buscador A*.
            A_star(mapa, no inicial, direcao inicial, no final) -> Buscador A*. '''
        self.mapa      = mapa
        self.max_x     = len(mapa[0])-1
        self.max_y     = len(mapa)-1
        self.no_ini    = no_ini
        self.no_fim    = no_fim
        no_ini.direcao = dir_ini
        self._start()

    def _start(self):
        ''' Inicia uma nova busca: Apaga todos os custos acumulados e limpa a heap. '''
        # Insere a posicao inicial
        self.fronteira = [(0, self.no_ini)]

        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                self.mapa[y][x].custo_acumulado = None
                self.mapa[y][x].prioridade = 9999999

        self.no_ini.custo_acumulado = 0
        self.no_ini.prioridade = 0

    def step(self):
        ''' Executa a proxima itaracao da busca: Retorna True se terminou a busca. '''

        if len(self.fronteira) == 0:
            return None

        atual = heapq.heappop(self.fronteira)[1] # elem da heap = (custo, No)

        if atual == self.no_fim:
            return None

        viz = self._vizinhos(atual)
        for v in viz:
            custo = atual.custo_acumulado + v.custo + self._rotacoes(atual, v, atual.direcao)
            if v.custo_acumulado == None or v.custo_acumulado > custo:
                prioridade = custo + self._distancia(self.no_fim, v)
                v.custo_acumulado = custo           # Custo de ir de no_ini ate v
                v.prioridade = prioridade           # Prioridade na heap
                v.anterior = atual                  # De onde viemos
                v.direcao = self.direcao(atual, v)  # Direcao que andamos para chegar em v
                heapq.heappush(self.fronteira, (prioridade, v))

        return (atual, viz)

    def run(self):
        ''' Executa todas as iteracoes da busca. '''
        while self.step():
            pass

