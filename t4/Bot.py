from INF1771_GameClient import HandleClient
from GameAI import AIController
import threading
import time

class GameBot(threading.Thread):
    def __init__(self, name=None, color=None):
        ''' Create bot. name = string, color = tuple (R[0-255], G[0-255], B[0-255]) '''
        super().__init__()
        self.alive = threading.Event()
        self.alive.set()
        self.interval = 0.5
        self.ai = AIController()
        self.game = HandleClient(self.__disconnectCB)
        self.game.setAIController(self.ai)

        self.actions = {"virar_direita"  : self.game.sendTurnRight,
                        "virar_esquerda" : self.game.sendTurnLeft,
                        "andar"          : self.game.sendForward,
                        "atacar"         : self.game.sendShoot,
                        "pegar_ouro"     : self.game.sendGetItem,
                        "pegar_anel"     : self.game.sendGetItem,
                        "pegar_powerup"  : self.game.sendGetItem,
                        "andar_re"       : self.game.sendBackward
                       }

        #self.game.connect("127.0.0.1")
        self.game.connect("atari.icad.puc-rio.br")
        if name:
            self.game.sendName(name)

        if color:
            self.game.sendColor(color)

        self.start()

    def __disconnectCB(self):
        self.alive.clear()

    def run(self):
        while self.alive.is_set():
            self.game.sendRequestGameStatus()
            self.game.recv(0.5) # Wait response

            # Read all pending messages
            while self.game.recv(0):
                pass

            if self.game.gameState == "Game":
                self.doDecision()

            time.sleep(self.interval)

    def doDecision(self):
        ''' Ask AI for the next action '''
        a = self.ai.getDecision()
        print("Decision: "+a) # Debug / requisito

        f = self.actions.get(a)
        if f:
            f()
        self.game.sendRequestUserStatus()
        self.game.sendRequestObservation()

    def close(self):
        self.alive.clear()
        if self.is_alive():
            self.join()
        self.game.sendGoodbye()

