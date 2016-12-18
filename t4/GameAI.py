import random

class AIController:
    def __init__(self):
        self.gameState = "Disconnected"
        self.time = 0

    def gameStatus(self, status, time):
        ''' Game status was updated '''
        self.gameState = status
        self.time = time

        print("game status", status, time)

    def scoreBoard(self, players):
        ''' Score Board was updated '''
        print("score board update")

    def playerStatus(self, pos, direction, state, score, health):
        ''' Our status was updated '''
        self.pos = pos
        self.direction = direction
        self.state = state
        self.score = score
        self.health = health

        print("player status:", pos, direction, state, score, health) # Debug

    def observation(self, o):
        ''' Observation result '''
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
                pass

            elif (obs == "redLight"):
                pass

            elif (obs == "greenLight"):
                pass

            elif (obs == "weakLight"):
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

