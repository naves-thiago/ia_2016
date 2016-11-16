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

    def atualiza(self):
        ''' Le o estado do ator e o conhecimento do mapa do prolog. '''
        self._atualiza_mapa()
        query = self._query("posicao(p(X, Y))")
        r = next(query)
        query.close()
        self.pos[0] = r['X'] - 1
        self.pos[1] = 12 - r['Y']

        query = self._query("vida(X)")
        r = next(query)
        query.close()
        self.vida = r['X']

        query = self._query("pontos(X)")
        r = next(query)
        query.close()
        self.pontos = r['X']

        query = self._query("direcao(X)")
        r = next(query)
        query.close()
        self.dir = r['X']

        # Teste
        #print("Pos: %s\nVida: %d\nPontos: %d\nDir: %s\n" % (str(self.pos), self.vida, self.pontos, self.dir))

    def _atualiza_mapa(self):
        ''' Atualiza o mapa com o conhecimento do prolog. '''
        for p in self._query("buraco(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'P')

        for p in self._query("teleport(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'T')

        for p in self._query("inimigoD(p(X, Y), _)"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'D')

        for p in self._query("inimigod(p(X, Y), _)"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'd')

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

