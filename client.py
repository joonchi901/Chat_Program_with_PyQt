from threading import *
from socket import *
from PyQt5.QtCore import *

class serverID:
    ip = '127.0.0.1'
    port = 1234
    size = 1024
    addr = (ip, port)

class Signal(QObject):
    recv_signal = pyqtSignal(str)

class ClientSocket:

    def __init__(self, parent):
        self.parent = parent

        self.recv = Signal()
        self.recv.recv_signal.connect(self.parent.update)


        self.bConnect = False

    def __del__(self):
        self.stop()

    def connectServer(self, ip, port):
        self.client = socket(AF_INET, SOCK_STREAM)

        try:
            self.client.connect((ip, port))
        except Exception as e:
            print('Connect Error : ', e)
            return False
        else:
            self.bConnect = True
            self.t = Thread(target=self.receive, args=(self.client,))
            self.t.start()
            print('Connected')

        return True

    def stop(self):
        self.bConnect = False
        if hasattr(self, 'client'):
            self.client.close()
            del (self.client)
            print('Client Stop')
            self.disconn.disconn_signal.emit()

    def receive(self, client):
        while self.bConnect:
            try:
                recv = client.recv(1024)
            except Exception as e:
                print('Recv() Error :', e)
                break
            else:
                msg = str(recv, encoding='utf-8')
                if msg:
                    self.recv.recv_signal.emit(msg)
                    print('[RECV]:', msg)

        self.stop()

    def send(self, msg):
        if not self.bConnect:
            return

        try:
            self.client.send(msg.encode())
        except Exception as e:
            print('Send() Error : ', e)