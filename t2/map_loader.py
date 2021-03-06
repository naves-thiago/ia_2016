import sys

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

        pl_map.write(":- dynamic([\n")
        pl_map.write("\tm_inimigoD/2,\n")
        pl_map.write("\tm_inimigod/2,\n")
        pl_map.write("\tm_powerup/1,\n")
        pl_map.write("\tm_buraco/1,\n")
        pl_map.write("\tm_teleport/1,\n")
        pl_map.write("\tm_ouro/1\n")
        pl_map.write("]).\n\n")

        # Cria nos para as posicoes livres do mapa
        for y in range(self.max_y+1):
            linha = []
            self.mapa.append(linha)
            for x in range(self.max_x+1):
                linha.append(No(x, y, mapa_s[y][x]))
                # sprites = {'D':sprite_enemy1, 'd':sprite_enemy2,   'U':sprite_powerup,
                #           'P':sprite_hole,   'T':sprite_teleport, 'O':sprite_gold}
                if (mapa_s[y][x]=='D'):
                    print('Assert: m_inimigoD(p(%d,%d),100).' %(x+1, 12-y))
                    pl_map.write('m_inimigoD(p(%d,%d),100).\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='d'):
                    print('Assert: m_inimigod(p(%d,%d),100).' %(x+1, 12-y))
                    pl_map.write('m_inimigod(p(%d,%d),100).\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='U'):
                    print('Assert: m_powerup(p(%d,%d)).' %(x+1, 12-y))
                    pl_map.write('m_powerup(p(%d,%d)).\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='P'):
                    print('Assert: m_buraco(p(%d,%d)).' %(x+1, 12-y))
                    pl_map.write('m_buraco(p(%d,%d)).\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='T'):
                    print('Assert: m_teleport(p(%d,%d)).' %(x+1, 12-y))
                    pl_map.write('m_teleport(p(%d,%d)).\n' %(x+1, 12-y))
                elif (mapa_s[y][x]=='O'):
                    print('Assert: m_ouro(p(%d,%d)).' %(x+1, 12-y))
                    pl_map.write('m_ouro(p(%d,%d)).\n' %(x+1, 12-y))
        pl_map.close()

#Teste
#ml   = MapLoader('mapa.txt')
