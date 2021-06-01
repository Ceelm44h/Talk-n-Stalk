import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from tns_client import Client

class ClientWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Talk\'n\'stalk'
        self.left = 20
        self.top = 10
        self.width = 750
        self.height = 400
        self.init_UI()
    
    def set_client(self, client):
        self.client = client

    def init_UI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        self.inputBox = QLineEdit(self)
        self.inputBox.move(20, 350)
        self.inputBox.resize(500,40)
        
        self.button = QPushButton('Send', self)
        self.button.move(520, 350)
        self.button.resize(60, 40)

        self.label = QLabel("przykladowy text", self)
        self.label.move(20, 20)
        self.label.resize(500, 200)
        self.label.setWordWrap(True)

        self.button.clicked.connect(self.on_send)
        self.show()

    @pyqtSlot()
    def on_send(self):
        textboxValue = self.inputBox.text()
        self.on_get(textboxValue)
        self.client.send(textboxValue)
    
    def on_get(self, msg):
        self.inputBox.setText("")
        self.label.setText(self.label.text() + '\n' + msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.exit(app.exec_())