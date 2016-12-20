import heapq
from mapa import No, TileType

class A_star:
    def _vizinhos(self, no):
        ''' Retorna a lista de vizinhos do No. Permite que um No desconhecido (tipo = '?')
            seja destino, mas nao permite passar por um desconhecido (nao retorna nenhum
            vizinho de um No desconhecido).'''
        if no.tipo == TileType.UNKNOWN:
            return []

        res = []
        x, y = no.pos
        if x > 0 and (self.mapa[y][x-1].tipo == TileType.FREE or self.mapa[y][x-1].tipo == TileType.UNKNOWN):
            res.append(self.mapa[y][x-1])

        if x < self.max_x and (self.mapa[y][x+1].tipo == TileType.FREE or self.mapa[y][x+1].tipo == TileType.UNKNOWN):
            res.append(self.mapa[y][x+1])

        if y > 0 and (self.mapa[y-1][x].tipo == TileType.FREE or self.mapa[y-1][x].tipo == TileType.UNKNOWN):
            res.append(self.mapa[y-1][x])

        if y < self.max_y and (self.mapa[y+1][x].tipo == TileType.FREE or self.mapa[y+1][x].tipo == TileType.UNKNOWN):
            res.append(self.mapa[y+1][x])

        return res

    @staticmethod
    def _distancia(a, b):
        ''' Calcula a distancia manhattan entre os Nos a e b. '''
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
    @staticmethod
    def rotacoesHora(orig, dest, direcao):
        ''' Calcula quantas rotacoes fazer para ir de orig para dest,
            considerando que so podemos rodar em sentido horario.
            rotacoes(orig, dest, direcao) -> numero de rotacoes. '''
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

        o = A_star._num_rotacao[direcao]
        d = A_star._num_rotacao[A_star.direcao(orig, dest)]

        return (d - o + 4) % 4

    @staticmethod
    def rotacoes(orig, dest, direcao):
        ''' Calcula quantas rotacoes fazer para ir de orig para dest.
            direcao é a direção ('U', 'D', 'L', 'R') em orig.
            rotacoes(orig, dest, direcao) -> numero de rotacoes. '''

        r = A_star.rotacoesHora(orig, dest, direcao)
        if r == 3:
            r = 1

        return r

    @staticmethod
    def seqRotacoes(orig, dest, direcao):
        ''' Calcula quais rotacoes fazer para ir de orig para dest.
            direcao é a direção ('U', 'D', 'L', 'R') em orig.
            rotacoes(orig, dest, direcao) -> tupla de rotacoes. '''

        r = A_star.rotacoesHora(orig, dest, direcao)
        return ((), ('R'), ('R', 'R'), ('L'))[r]  # 3 rotacoes a direita = 1 a esquerda

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
            custo = atual.custo_acumulado + v.custo + self.rotacoes(atual, v, atual.direcao)
            if v.custo_acumulado == None or v.custo_acumulado > custo:
                prioridade = custo + self._distancia(self.no_fim, v)
                v.custo_acumulado = custo           # Custo de ir de no_ini ate v
                v.prioridade = prioridade           # Prioridade na heap
                v.anterior = atual                  # De onde viemos
                v.direcao = self.direcao(atual, v)  # Direcao que andamos para chegar em v
                heapq.heappush(self.fronteira, (prioridade, v))

        return (atual, viz)

    def run(self):
        ''' Executa todas as iteracoes da busca e retorna a sequencia de acoes para ir
        ate o destino. '''
        while self.step():
            pass

        dest = self.no_fim
        # Procurando um No nao visitado?
        if self.no_fim == None:
            dest = self.__findUnvisited()

        # Nao tem pra onde ir...
        if dest == None:
            return None

        return self.__stepsDest(dest)

    def __findUnvisited(self):
        # Encontra todos os nao visitados alcancaveis
        candidatos = []
        for y in self.mapa:
            for x in y:
                if x.tipo == TileType.UNKNOWN and x.custo_acumulado != None:
                    candidatos.append(x)

        # Econtra o No mais proximo entre os candidatos
        if len(candidatos) == 0:
            return None

        melhor = candidatos[0]
        for c in candidatos:
            if c.custo_acumulado < melhor.custo_acumulado:
                melhor = c

        return melhor

    def __stepsDest(self, dest):
        ''' Retorna a sequencia de passos para chegar no No dest '''
        pos   = [] # Sequencia de posicoes
        steps = [] # Sequencia de acoes (vira, anda...)
        a = dest
        while a:
            pos.insert(0, a)
            if a == self.no_ini:
                break
            a = a.anterior

        for i in range(len(pos)-1):
            # Roda o numero de vezes necessario
            steps.extend(A_star.seqRotacoes(pos[i], pos[i+1], pos[i].direcao))
            steps.append("F") # Anda pra frente

        return steps


