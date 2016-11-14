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
            pl_map = file("mapa.pl", 'w')
        else:
            mf = open(arquivo)
            pl_map = open("mapa.pl", 'w')

        mapa_s = mf.readlines()
        mf.close()
        if sys.version_info[0] < 3:
            self.max_x = len(mapa_s[0])-3 # Remove \r\n
        else:
            self.max_x = len(mapa_s[0])-2 # Remove \n

        self.max_y = len(mapa_s)-1

        pl_map.write(":-dynamic([\n")
        pl_map.write("\tinimigoD/2,\n")
        pl_map.write("\tinimigod/2,\n")
        pl_map.write("\tpowerup/1,\n")
        pl_map.write("\tburaco/1,\n")
        pl_map.write("\tteleport/1,\n")
        pl_map.write("\touro/1,\n")
        pl_map.write("]).\n\n")

        # Cria nos para as posicoes livres do mapa
        for y in range(self.max_y+1):
            linha = []
            self.mapa.append(linha)
            for x in range(self.max_x+1):
                linha.append(No(x+1, 12-y, mapa_s[y][x]))
                # sprites = {'D':sprite_enemy1, 'd':sprite_enemy2,   'U':sprite_powerup,
                #           'P':sprite_hole,   'T':sprite_teleport, 'O':sprite_gold}
                if (mapa_s[y][x]=='D'):
                    print 'inimigoD(p(',x+1,',',y+1,'),100)'
                    pl_map.write('inimigoD(p(%d,%d),100)\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='d'):
                    print 'inimigod(p(%d,%d),100)' %(x+1, 12-y)
                    pl_map.write('inimigod(p(%d,%d),100)\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='U'):
                    print 'powerup(p(%d,%d))' %(x+1, 12-y)
                    pl_map.write('powerup(p(%d,%d))\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='P'):
                    print 'buraco(p(%d,%d))' %(x+1, 12-y)
                    pl_map.write('buraco(p(%d,%d))\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='T'):
                    print 'teleport(p(%d,%d))' %(x+1, 12-y)
                    pl_map.write('teleport(p(%d,%d))\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='O'):
                    print 'ouro(p(%d,%d))' %(x+1, 12-y)
                    pl_map.write('ouro(p(%d,%d))\n' %(x+1, 12-y))
        pl_map.close()

ml   = MapLoader('mapa.txt')