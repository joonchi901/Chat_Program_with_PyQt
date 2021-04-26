from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from socket import *
import client

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.s = client.ClientSocket(self)
        self.s.connectServer('127.0.0.1', 1234)

        self.initUI()

    def initUI(self):
        self.setWindowTitle('채팅3')

        vbox = QVBoxLayout()

        lbl = QLabel('메세지 창')
        vbox.addWidget(lbl)

        self.msg = QTextEdit()
        self.msg.setReadOnly(True)
        vbox.addWidget(self.msg)

        lbl = QLabel('보낼 메세지')
        vbox.addWidget(lbl)

        self.sendmsg = QLineEdit()
        self.sendmsg.returnPressed.connect(self.sendMsg)
        vbox.addWidget(self.sendmsg)

        hbox = QHBoxLayout()

        self.sendbtn = QPushButton('보내기')
        self.sendbtn.clicked.connect(self.sendMsg)
        hbox.addWidget(self.sendbtn)

        self.clearbtn = QPushButton('채팅창 지움')
        self.clearbtn.clicked.connect(self.clearMsg)
        hbox.addWidget(self.clearbtn)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.show()

    def update(self, msg):
        self.msg.append('상대방 : ' + msg)
        self.msg.setAlignment(Qt.AlignLeft)

    def updateMsg(self, msg):
        self.msg.append(msg + ' : 나')
        self.msg.setAlignment(Qt.AlignRight)

    def sendMsg(self):
        sendmsg = self.sendmsg.text()
        if sendmsg != "":
            self.s.send(sendmsg)
            self.updateMsg(sendmsg)
            self.sendmsg.clear()

    def clearMsg(self):
        self.msg.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())