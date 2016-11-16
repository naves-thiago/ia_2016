import pyswip
from map_loader import No

class PrologActor:
    def __init__(self, arquivo):
        self.pl = pyswip.Prolog()
        self.pl.consult(arquivo)

        # Cria um mapa vazio
        mapa = []
        for y in range(12):
            linha = []
            for x in range(12):
                linha.append(No(x, y, '?'))

            mapa.append(linha)

        self.mapa   = mapa
        self.pos    = [0, 11] # Posicao convertida do ator
        self.dir    = "U"     # Direcao do ator
        self.vida   = 100
        self.pontos = 0
        self.ouros  = 0
        self.balas  = 5

        self.atualiza()

    def andar_frente(self):
        # FIXME
        if self.dir == "R":
            self.pos[0] += 1
        elif self.dir == "L":
            self.pos[0] -= 1
        elif self.dir == "U":
            self.pos[1] -= 1
        else:
            self.pos[1] += 1

        print("POS: " + str(self.pos) + "  - " + self.dir)

    def rodar(self):
        # FIXME
        if self.dir == "R":
            self.dir = "D"
        elif self.dir == "L":
            self.dir = "U"
        elif self.dir == "U":
            self.dir = "R"
        else:
            self.dir = "L"

    def acao(self, a):
        # TODO completar
        if a == "A":
            self.andar_frente()
        else:
            self.rodar()

    def melhor_acao(self):
        ''' Consulta qual e a melhor acao a fazer. '''
        query = self._query("prox(X)")
        r = next(query)
        query.close()
        return r["X"]

    def _muda_no(self, x, y, tipo):
        ''' Troca o tipo de um No do mapa, convertendo as coordenadas do prolog. '''
        # Converte coordenadas
        x = x -1
        y = 12 - y
        self.mapa[y][x].tipo = tipo

    def _query(self, qry):
        ''' Faz uma consulta no prolog e imprime a consulta no console. '''
        #print("Query: " + qry)
        return self.pl.query(qry)

    def _query_single(self, qry):
        ''' Faz uma consulta no prolog e le apenas o primeiro resultado. '''
        query = self._query(qry)
        r = next(query)
        query.close()
        return r

    def atualiza(self):
        ''' Le o estado do ator e o conhecimento do mapa do prolog. '''
        self._atualiza_mapa()
        r = self._query_single("posicao(p(X, Y))")
        self.pos[0] = r['X'] - 1
        self.pos[1] = 12 - r['Y']

        r = self._query_single("vida(X)")
        self.vida = r['X']

        r = self._query_single("pontos(X)")
        self.pontos = r['X']

        r = self._query_single("direcao(X)")
        self.dir = r['X']

        r = self._query_single("o_coletados(X)")
        self.ouros = r["X"]

        r = self._query_single("balas(X)")
        self.balas = r["X"]

    def _atualiza_mapa(self):
        ''' Atualiza o mapa com o conhecimento do prolog. '''
        for p in self._query("pburaco(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'P')

        for p in self._query("pteleport(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'T')

        for p in self._query("pinimigo(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'D')

        for p in self._query("powerup(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'U')

        for p in self._query("ouro(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'O')

        for p in self._query("livre(X, Y)"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, '.')

