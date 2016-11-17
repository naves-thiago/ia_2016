import pyswip
from map_loader import No

class PrologActor:
    def __init__(self, arquivo):
        self.pl = pyswip.Prolog()
        self.pl.consult(arquivo)
        self._query_single("reset")

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
        self._query_single("andar")
        # print("POS: " + str(self.pos) + "  - " + self.dir) ### DEBUG

    def rodar(self):
        self._query_single("virar")

    def pegar_item(self):
        tipo = self.mapa[self.pos[1]][self.pos[0]].tipo
        if tipo == "U":
            self._query_single("pegar_powerup")
        elif tipo == "O":
            # print("Pegar ouro") #### DEBUG
            self._query_single("pegar_ouro")

    def atirar(self):
        self._query_single("atirar")

    def exec_acao(self, a):
        if a == "A":
            self.andar_frente()
        elif a == "R":
            self.rodar()
        elif a == "P":
            self.pegar_item()
        elif a == "T":
            self.atirar()

    def sair(self):
        print("Query: sair")
        self.pl.query("sair")

    def melhor_acao(self):
        ''' Consulta qual e a melhor acao a fazer. '''
        query = self._query("prox(X)")
        r = next(query)
        query.close()
        # print("ACAO: " + r["X"]) #### DEBUG
        return r["X"]

    def observar(self):
        ''' Leitura dos sensores... '''
        self._query_single("observar")
        self.atualiza()

    def _muda_no(self, x, y, tipo):
        ''' Troca o tipo de um No do mapa, convertendo as coordenadas do prolog. '''
        # Converte coordenadas
        x = x -1
        y = 12 - y
        self.mapa[y][x].tipo = tipo

    def _query(self, qry):
        ''' Faz uma consulta no prolog e imprime a consulta no console. '''
        print("Query: " + qry)
        return self.pl.query(qry)

    def _query_single(self, qry):
        ''' Faz uma consulta no prolog e le apenas o primeiro resultado. '''
        print("Query: " + qry)
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

        for p in self._query("livre(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, '.')

        for p in self._query("powerup(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'U')

        for p in self._query("ouro(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'O')

