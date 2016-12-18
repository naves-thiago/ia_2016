'''
Comandos do servidor:

* w sendForward(); – anda para frente
* s sendBackward(); – anda de ré
* a sendTurnLeft(); – virar a esquerda 90º
* d sendTurnRight(); – virar a direita 90º
* t sendGetItem(); – pegar item
* e sendShoot(); – atirar
* o sendRequestObservation(); – receber observações (separado por ; e , )
* g sendRequestGameStatus(); – receber o status do jogo (estado, tempo atual)
* q sendRequestUserStatus(); – receber status do usuário (posição, estado do agente, pontos e energia)
* p sendRequestPosition(); – receber posição do agente
* u sendRequestScoreboard(); – lista de usuários logados e pontos
* quit sendGoodbye(); – desconectar do jogo
* name params[1]: name sendName – trocar de nome
* say params[1]: msg sendSay – enviar mensagem
* color params[3]: r(0-255), g(0-255), b(0-255) sendColor, sendColor(color) – trocar de cor
'''

from socket import socket
import threading
import queue

class StringSocket(threading.Thread):
    def __init__(self, closeCallback=None):
        super().__init__()
        self.closeCallback = closeCallback
        self.buff_len = 100
        self.timeout  = 0.1
        self.socket = socket()
        self.alive = threading.Event()
        self.alive.clear()
        self.send_queue = queue.Queue()
        self.recv_queue = queue.Queue()
        self.msg = ""

    def run(self):
        self.alive.wait() # Wait for a connection

        while self.alive.is_set():
            try:
                r = self.__recv()
                if len(r) == 0:
                    self.alive.clear()
                    self.socket.close()
                    if self.closeCallback:
                        self.closeCallback()

                    return

                self.__parse(r)
            except BlockingIOError as e:
                pass

            try:
                s = self.send_queue.get(True, self.timeout)
                self.__send(s)
            except:
                pass


    def __del__(self):
        self.close()

    def connect(self, host):
        self.socket.connect(host)
        self.socket.setblocking(0)
        self.alive.set() # Start thread loop
        self.start()

    def close(self):
        self.alive.clear()
        if self.is_alive():
            self.join() # Wait thread termination
        self.socket.close()

    def send(self, s):
        self.send_queue.put(s)

    def recv(self, timeout=None):
        try:
            return self.recv_queue.get(True, timeout)
        except:
            return None

    def __parse(self, s):
        # Join with last reception (in case it was partial)
        tmp = self.msg + s

        # Split received data into lines
        l = tmp.split("\n")

        # Store the last line. Empty if we received whole messages,
        # or a partial message otherwise
        self.msg = l.pop()

        # Add each message (line) to the reception queue
        for m in l:
            self.recv_queue.put(m)

    def __send(self, s):
        self.socket.send(bytes(s, 'utf-8'))

    def __recv(self):
        return self.socket.recv(self.buff_len).decode('utf-8')


class HandleClient:
    def __init__(self):
        self.socket = StringSocket()
        self.ai = None # AIController instance
        self.connected = False
        self.interval = 1
        self.players = {}
        self.gameState = "Disconnected"
        self.lastHitBy = None
        self.lastHit = None
        self.lastObservation = ""
        self.state = "game"
        self.health = 100
        self.score = 0
        self.pos = [0, 0] # [x, y]
        self.direction = "north"
        self.name = None
        self.parsers = {'g': self.__updateGameStatus,
                        'u': self.__updateScoreBoard,
                        'd': self.__takeDamage,
                        'h': self.__hitPlayer,
                        's': self.__updatePlayerStatus,
                        'o': self.__observation,
                        'hello' : self.__connected,
                        'goodbye' : self.__playerQuit,
                        'changename' : self.__playerRename,
                        'notification' : self.__chatReceived
                       }

    def __del__(self):
        self.sendGoodbye()

    def __connectionClosedCallback(self):
        self.connected = False
        self.ai.gameStatus("Disconnected", self.time)

    def _send(self, s):
        self.socket.send(s+'\n')

    def __recv(self):
        ''' Requests a message from the socket '''
        self.__parse(self.socket.recv())

    def __parse(self, s):
        ''' Parse server message and update state '''
        r = s.split(";")
        p = self.parsers.get(r[0])
        if not p:
            print("Unkown message: " + s)
            return

        p(r[1:])

    def __updateGameStatus(self, s):
        ''' "g" message '''
        self.gameState = s[0]
        self.time  = int(s[1])
        self.ai.gameStatus(self.gameState, self.time)

    def __updateScoreBoard(self, s):
        ''' "u" message '''
        # Player 41#connected#0#100#Color [A=255, R=156, G=191, B=213]
        for p in s:
            t = p.split("#")
            d = {"status" : t[1],
                 "score"  : t[2],
                 "health" : t[3]
                }

            if len(t) == 5:
                d["color"] = t[4]
            else:
                d["color"] = "?"

            self.players[t[0]] = d

        self.ai.scoreBoard(self.players)

    def __updatePlayerStatus(self, s):
        ''' "s" message '''
        self.pos[0] = int(s[0])
        self.pos[1] = int(s[1])
        self.direction = s[2]
        self.state = s[3]
        self.score = int(s[4])
        self.health = int(s[5])
        self.ai.playerStatus(self.pos, self.direction, self.state, self.score,
                             self.health)

    def __observation(self, s):
        ''' "o" message '''
        self.lastObservation = s[0]
        self.ai.observation(s[0])

    def __connected(self, s):
        ''' "hello" message. Called when any player joins the server '''
        self.ai.playerConnected(s[0])

    def __takeDamage(self, s):
        ''' "d" message '''
        self.lastHitBy = s[0]
        self.ai.takeDamage(s[0])

    def __hitPlayer(self, s):
        ''' "h" message '''
        self.lastHit = s[0]
        self.ai.hitPlayer(s[0])

    def __playerQuit(self, s):
        ''' "goodbye" message '''
        p = self.players.get(s[0])
        if p:
            p["status"] = "offline"

        self.ai.playerQuit(s[0])

    def __playerRename(self, s):
        ''' "changename" message '''
        p = self.players.get(s[0])
        if p:
            self.players[s[1]] = p
            self.players.pop(s[0])

        self.ai.playerRename(s[0], s[1])

    def __chatReceived(self, s):
        ''' "notification" message '''
        self.ai.chat(s[0])

    def setAIController(self, ai):
        ''' Sets the AI controller instance. This must be called before connect. '''
        self.ai = ai
        ai.setHandleClient(self)

    def connect(self, host):
        ''' Connect to the game server on port 8888 '''
        if (self.ai == None):
            raise Exception("AI Controller not set.")

        self.socket.connect((host, 8888))
        self.connected = True
        while True:
            self.__recv()

    def sendForward(self):
        self._send('w')

    def sendBackward(self):
        self._send('s')

    def sendTurnLeft(self):
        self._send('a')

    def sendTurnRight(self):
        self._send('d')

    def sendGetItem(self):
        self._send('t')

    def sendShoot(self):
        self._send('e')

    def sendRequestObservation(self):
        res = self._send('o')

    def sendRequestGameStatus(self):
        res = self._send('g')

    def sendRequestUserStatus(self):
        res = self._send('q')

    def sendRequestPosition(self):
        res = self._send('p')

    def sendRequestScoreboard(self):
        res = self._send('u')

    def sendGoodbye(self):
        self._send('quit')
        self.socket.close()

    def sendName(self, name):
        self._send('name;' + name)
        self.name = name

    def sendColor(self, r, g, b):
        self._send('color;%d;%d;%d' % (r,g,b))

class AIController:
    def __init__(self):
        self.server = None # Game Server Handle
        self.gameState = "Disconnected"
        self.time = 0

    def setHandleClient(self, h):
        ''' Should only be called from within HandleClient. '''
        server = h

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
        print("observation", o) # Debug

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

def main():
    ai = AIController()
    g = HandleClient()
    g.setAIController(ai)
    g.connect("127.0.0.1")

main()
