import random
from a_star import A_star
from mapa import Mapa

class Acoes:
    PEGAR    = 0
    FRENTE   = 1
    ATRAS    = 2
    DIREITA  = 3
    ESQUERDA = 4
    ATIRAR   = 5

class AIController:
    def __init__(self):
        self.mapa = Mapa()
        self.gameState = "Disconnected"
        self.ultima_observacao = []
        self.time = 0
        self.proxAcao = Acoes.DIREITA

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

    def observation(self, o):
        ''' Observation result '''

        self.ultima_observacao = o

        for obs in o:
            print("observation", obs) # Debug

            if obs == "blocked":
                p = self.nextPosition()
                n = self.mapa.get(p[0], p[1])
                n.tipo = TileType.WALL

            elif obs == "steps":
                pass

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

                self.proxAcao = Acoes.PEGAR

            elif obs == "redLight":
                # Power-up
                n = self.mapa.get(self.pos[0], self.pos[1])
                n.tipo = TileType.GOLD
                if not n in self.mapa.ouros:
                    self.mapa.ouros.append(n)

                # Acao ?

            elif obs == "weakLight":
                # Indefinido. (acho que nao tem)
                pass

            elif a[:5] == "enemy":
                dist = int(a[6:])
                self.proxAcao = Acoes.ATIRAR

    def observationClean(self):
        ''' Observation result was nothing observated '''
        print("observation clean")

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
        action = ("pegar_ouro",
                  "andar",
                  "andar_re",
                  "virar_direita",
                  "virar_esquerda",
                  "atacar")

        return action[self.proxAcao]

