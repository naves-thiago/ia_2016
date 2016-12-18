import random
from a_star import A_star
from mapa import Mapa

class AIController:
    def __init__(self):
        self.mapa = Mapa()
        self.gameState = "Disconnected"
        self.ultima_observacao = []
        self.time = 0

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
        self.direction = _convert_dir[direction]
        self.state = state
        self.score = score
        self.health = health

        print("player status:", pos, direction, state, score, health) # Debug

    def nextPosition(self):
        ''' Retorna o No na posicao na frente da atual '''
        p = [x for x in self.pos] # Copia a posicao atual
        if self.direction == 'U':
            p[1] -= 1
        elif self.direction == 'D':
            p[1] += 1
        elif self.direction == 'L':
            p[0] -= 1
        else
            p[0] += 1

        return self.mapa.get(p[0], p[1])

    def observation(self, o):
        ''' Observation result '''

        self.ultima_observacao = o

        for obs in o:
            print("observation", obs) # Debug

            if (obs == "blocked"):
                pass

            elif (obs == "steps"):
                pass

            elif (obs == "breeze"):
                pass

            elif (obs == "flash"):
                pass

            elif (obs == "blueLight"):
                # Tesouro
                pass

            elif (obs == "redLight"):
                # Power-up
                pass

            elif (obs == "weakLight"):
                # Indefinido. (acho que nao tem)
                pass

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
        action = ("virar_direita",
                  "virar_esquerda",
                  "andar",
                  "atacar",
                  "pegar_ouro",
                  "pegar_anel",
                  "pegar_powerup",
                  "andar_re")

        return action[random.randint(0,7)]

