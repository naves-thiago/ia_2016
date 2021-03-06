import pdb
import random
from a_star import A_star
from mapa import Mapa, TileType

class Acoes:
    PEGAR    = 0
    FRENTE   = 1
    ATRAS    = 2
    DIREITA  = 3
    ESQUERDA = 4
    ATIRAR   = 5

class Objetivos:
    EXPLORAR  = 0
    OURO      = 1
    POWER_UP  = 2
    A_ESTRELA = 3

class AIController:
    def __init__(self):
        self.mapa = Mapa()
        self.gameState = "Disconnected"
        self.ultima_observacao = []
        self.time = 0
        self.acoes = [Acoes.FRENTE]
        self.objetivo = Objetivos.EXPLORAR
        self.ready = False
        #self.direction = 'U'
        #self.pos = (3,3) # gambiarra (nao sabemos nossa pos na primeira iteracao)

    def gameStatus(self, status, time):
        ''' Game status was updated '''
        self.gameState = status
        self.time = time

        print("game status", status, time)

    def scoreBoard(self, players):
        ''' Score Board was updated '''
        print("score board update")

    _convert_dir = {"north" : 'U', 'east' : 'R', 'south' : 'D', 'west' : 'L'}
    def playerStatus(self, pos, direction, state, score, health):
        ''' Our status was updated '''
        self.pos = pos
        self.direction = AIController._convert_dir[direction]
        self.state = state
        self.score = score
        self.health = health

        print("player status:", pos, direction, state, score, health) # Debug

    def nextPosition(self, dist=1):
        ''' Retorna o No dist posicoes na frente da atual '''
        p = [x for x in self.pos] # Copia a posicao atual
        if self.direction == 'U':
            p[1] -= dist
        elif self.direction == 'D':
            p[1] += dist
        elif self.direction == 'L':
            p[0] -= dist
        else:
            p[0] += dist

        return self.mapa.get(p[0], p[1])

    __convertePasso = {'F' : Acoes.FRENTE, 'R' : Acoes.DIREITA, 'L' : Acoes.ESQUERDA}
    def explorar(self):
        prox = self.nextPosition()
        if prox and self.mapa.isSafe(prox):
            self.acoes = [Acoes.FRENTE]
        else:
            # A* para o desconhecido mais proximo
            atual = self.mapa.get(self.pos[0], self.pos[1])
            a = A_star(self.mapa, atual, self.direction, None)
            seq = a.run() # Sequencia de passos

            # Converte o formato da sequencia retornada pelo A*
            print(seq)
            self.acoes = []
            if not seq or len(seq) == 0:
                return

            for s in seq:
                self.acoes.append(AIController.__convertePasso[s])

        self.objetivo = Objetivos.EXPLORAR

    def observation(self, o):
        ''' Observation result '''

        atual = self.mapa.get(self.pos[0], self.pos[1])
        self.mapa.flagLivre(atual)

        self.ultima_observacao = o

        for obs in o:
            print("observation", obs) # Debug

            if obs == "blocked":
                # Por agora considerando que so andamos para frente
                n = self.nextPosition()
                if n:
                    self.mapa.flagParede(n)

                if not "breeze" in o and not "flash" in o:
                    adj = self.mapa.adjacentes(self.pos)
                    for n in adj:
                        self.mapa.flagSafe(n)

                # Procura um novo caminho para o objetivo
                # TODO testar qual eh o objetivo
                self.explorar()

            elif obs == "steps":
                if len(o) == 1:
                    self.observationClean()

            elif obs == "breeze":
                adj = self.mapa.adjacentes(self.pos)
                for n in adj:
                    self.mapa.flagPBuraco(n)

            elif obs == "flash":
                adj = self.mapa.adjacentes(self.pos)
                for n in adj:
                    self.mapa.flagPTeleport(n)

            elif obs == "blueLight":
                # Tesouro
                n = self.mapa.get(self.pos[0], self.pos[1])
                n.tipo = TileType.GOLD
                if not n in self.mapa.ouros:
                    self.mapa.ouros.append(n)

                self.acoes.insert(0, Acoes.PEGAR)

                if not "breeze" in o and not "flash" in o:
                    adj = self.mapa.adjacentes(self.pos)
                    for n in adj:
                        self.mapa.flagSafe(n)

            elif obs == "redLight":
                # Power-up
                n = self.mapa.get(self.pos[0], self.pos[1])
                n.tipo = TileType.GOLD
                if not n in self.mapa.ouros:
                    self.mapa.ouros.append(n)

                if not "breeze" in o and not "flash" in o:
                    adj = self.mapa.adjacentes(self.pos)
                    for n in adj:
                        self.mapa.flagSafe(n)

                # Acao ?

            elif obs == "weakLight":
                # Indefinido. (nao tem)
                pass

            elif obs[:5] == "enemy":
                dist = int(obs[6:])
                self.acoes.insert(0, Acoes.ATIRAR)


        if len(self.acoes) == 0:
            self.explorar()

        if len(self.acoes) == 0:
            print("Sem acoes")
            self.acoes = [Acoes.DIREITA, Acoes.DIREITA, Acoes.FRENTE]

        self.mapa.printMap()

        self.ready = True

    def observationClean(self):
        ''' Observation result was nothing observated '''
        atual = self.mapa.get(self.pos[0], self.pos[1])
        adj = self.mapa.adjacentes(atual)
        self.mapa.flagLivre(atual)
        for n in adj:
            self.mapa.flagSafe(n)

        if len(self.acoes) == 0:
            self.explorar()

        if len(self.acoes) == 0:
            print("Sem acoes")
            self.acoes = [Acoes.DIREITA, Acoes.DIREITA, Acoes.FRENTE]

        self.mapa.printMap()

        self.ready = True

    def playerConnected(self, player):
        ''' A player joined the server '''
        print("player joined:", player)

    def takeDamage(self, shooter):
        ''' We got hit '''
        print("got hit by:", shooter)

    def hitPlayer(self, target):
        ''' We hit another player '''
        print("hit:", target)

    def playerQuit(self, player):
        ''' A player quit the server '''
        print("player quit:", player)

    def playerRename(self, oldName, newName):
        ''' A player changed the name '''
        print("player rename:", oldName, newName)

    def chat(self, message):
        ''' A chat message was received '''
        print("chat", message)

    def getDecision(self):
        ''' Return the next action '''
        if not self.ready:
            return ""

        self.ready = False

        action = ("pegar_ouro",
                  "andar",
                  "andar_re",
                  "virar_direita",
                  "virar_esquerda",
                  "atacar")

        print("acoes: " + str(self.acoes))
        if len(self.acoes) > 0:
            if self.acoes[0] == Acoes.FRENTE:
                n = self.nextPosition()
                if n and not self.mapa.isSafe(n):
                    self.acoes = []
                    print("Nao se mata xD")
                    return ""

            a = self.acoes.pop(0)
            print("---> Pop " + action[a]) # DEBUG
            print("acoes: " + str(self.acoes))
        else:
            #print("---> EXPLORAR")  # DEBUG
            print("Sem acao") # DEBUG
            return ""

        return action[a]

