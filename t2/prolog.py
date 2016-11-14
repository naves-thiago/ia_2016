import pyswip
from map_loader import No

class PrologMap:
    def __init__(self):
        self.pl = pyswip.Prolog()
        #self.pl.consult("db.pl")
        self.pl.consult("teste.pl")

        # Cria um mapa vazio
        mapa = []
        for y in range(12):
            linha = []
            for x in range(12):
                linha.append(No(x, y, '?'))

            mapa.append(linha)

        self.mapa = mapa

    def _muda_no(self, x, y, tipo):
        # Converte coordenadas
        x = x -1
        y = 12 - y
        self.mapa[y][x].tipo = tipo

    def atualiza_mapa(self):
        for p in self.pl.query("buraco(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'P')

        for p in self.pl.query("teleport(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'T')

        for p in self.pl.query("inimigoD(p(X, Y), _)"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'D')

        for p in self.pl.query("inimigod(p(X, Y), _)"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'd')

        for p in self.pl.query("powerup(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'U')

        for p in self.pl.query("ouro(p(X, Y))"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, 'O')

        for p in self.pl.query("livre(X, Y)"):
            x = p['X']
            y = p['Y']
            self._muda_no(x, y, '.')

