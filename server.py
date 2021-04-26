from threading import *
from socket import *
from PyQt5.QtCore import *

class serverID:
    ip = ''
    port = 1234
    size = 1024
    addr = (ip, port)

class Signal(QObject):
    recv_signal = pyqtSignal(str)

class ServerSocket:

    def __init__(self, parent):
        self.parent = parent
        self.bListen = False
        self.ip = serverID.ip
        self.port = serverID.port
        self.addr = serverID.addr
        self.clients = []
        self.threads = []

        self.recv = Signal()

        self.recv.recv_signal.connect(self.parent.update)

    def __del__(self):
        self.stop()

    def start(self):
        self.server = socket(AF_INET, SOCK_STREAM)

        try:
            self.server.bind(self.addr)
        except Exception as e:
            print('Bind Error : ', e)
            return False
        else:
            self.bListen = True
            self.t = Thread(target=self.listen, args =(self.server,))
            self.t.start()
            print('server listening')

        return True

    def stop(self):
        self.bListen = False
        if hasattr(self, 'server'):
            self.server.close()
            print('Server Stop')

    def listen(self, server):
        while self.bListen:
            server.listen()
            try:
                client, addr = server.accept()
            except Exception as e:
                print('Accept() Error : ', e)
                break
            else:
                self.recv.recv_signal.emit('유저가 접속했습니다.')
                self.clients.append(client)
                t = Thread(target=self.receive, args=(addr, client))
                self.threads.append(t)
                t.start()
        self.removeAllClients()
        self.server.close()

    def receive(self, addr, client):
        while True:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.send(msg)
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]:', addr, msg)

        self.removeClient(client)


    def send(self, msg):
        try:
            for c in self.clients:
                c.send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)

    def removeClient(self, client):
        client.close()
        self.clients.remove(client)
        i = 0
        for t in self.threads[:]:
            if not t.isAlive():
                del (self.threads[i])
            i += 1

    def removeAllClients(self):
        for c in self.clients:
            c.close()

        self.clients.clear()
        self.threads.clear()



