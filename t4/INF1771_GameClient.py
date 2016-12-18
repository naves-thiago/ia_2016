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
from weakref import WeakMethod

class StringSocket(threading.Thread):
    ''' Threaded socket connection that expects to receive lines ending in \\n. Has send and receive queues for buffering and thread synchronization '''
    def __init__(self, closeCallback=None):
        super().__init__()
        if closeCallback:
            # Weak reference to avoid a circular reference messing with __del__()
            self.closeCallback = WeakMethod(closeCallback)
        else:
            self.closeCallback = None
        self.buff_len = 100 # receive from socket buffer size
        self.timeout  = 0.1 # get from send_queue timeout. Limits CPU usage
        self.socket = socket()
        self.alive = threading.Event()
        self.alive.clear()
        self.send_queue = queue.Queue()
        self.recv_queue = queue.Queue()
        self.msg = ""  # Partially received message

    def run(self):
        ''' Thread entry point (called by start() in connect() '''
        self.alive.wait() # Wait for a connection

        while self.alive.is_set():
            try:
                r = self.__recv()
                if len(r) == 0:
                    self.alive.clear()
                    self.socket.close()
                    if self.closeCallback and self.closeCallback():
                        self.closeCallback()()

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
        ''' Connects to the host (tuple (hostname / ip, port)) and starts the thread '''
        self.socket.connect(host)
        self.socket.setblocking(0)
        self.alive.set() # Start thread loop
        self.start()

    def close(self):
        ''' Stops the thread and closes the socket '''
        self.alive.clear()  # Request thread termination
        if self.is_alive(): # Test if the thread is running
            self.join()     # Wait thread termination
        self.socket.close()

    def send(self, s):
        ''' Queue data to send '''
        self.send_queue.put(s)

    def recv(self, timeout=None):
        ''' Read from the receive queue with optional timeout '''
        try:
            if timeout == 0:
                return self.recv_queue.get(False)
            else:
                return self.recv_queue.get(True, timeout)
        except:
            return None

    def __parse(self, s):
        ''' Split data on \\n and join partial messages '''
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
        ''' Convert string to bytes and send them '''
        self.socket.send(bytes(s, 'utf-8'))

    def __recv(self):
        ''' Convert received bytes to string '''
        return self.socket.recv(self.buff_len).decode('utf-8')


class HandleClient:
    ''' INF1771 Game Client class '''
    def __init__(self, disconnectListener = None):
        if disconnectListener:
            self.disconnectListener = WeakMethod(disconnectListener)
        else:
            self.disconnectListener = None
        self.socket = StringSocket()
        self.ai = None # AIController instance
        self.connected = threading.Event()
        self.connected.clear()
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
        self.connected.clear()
        if self.disconnectListener:
            cb = self.disconnectListener()
            if cb:
                cb()
        self.ai.gameStatus("Disconnected", self.time)

    def _send(self, s):
        self.socket.send(s+'\n')

    def recv(self, timeout=None):
        ''' Requests a message from the socket. Return True on success, False on timeout '''
        m = self.socket.recv(timeout)
        if m:
            self.__parse(m)
            return True
        else:
            return False

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
        if len(s) > 0 and s[0] != '':
            self.lastObservation = s
            self.ai.observation(s)
        else:
            self.ai.observationClean()

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

    def connect(self, host):
        ''' Connect to the game server on port 8888 '''
        if (self.ai == None):
            raise Exception("AI Controller not set.")

        self.socket.connect((host, 8888))
        self.connected.set()

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
        self.connected.clear()
        self.socket.close()

    def sendName(self, name):
        self._send('name;' + name)
        self.name = name

    def sendColor(self, rgb):
        self._send('color;%d;%d;%d' % rgb)

