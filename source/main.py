import sys
import random
import string
from PySide6 import QtCore, QtWidgets, QtGui
LETTERS = [chr(i) for i in range(65, 89)]
class homeMenu(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.laying = QtWidgets.QVBoxLayout(self)
        self.edgeButton = QtWidgets.QPushButton("Edge Menu")
        self.cornerButton = QtWidgets.QPushButton("Corner Menu")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        self.laying.addWidget(self.text)
        self.laying.addWidget(self.edgeButton)
        self.laying.addWidget(self.cornerButton)
        self.edgeButton.clicked.connect(lambda: controller.setPage(1, True, "A"))
        self.cornerButton.clicked.connect(lambda: controller.setPage(1, False, "A"))
class commMenu(QtWidgets.QWidget):
    def __init__(self, controller, pieceType: bool, letter: str):
        super().__init__()
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        self.letter = QtWidgets.QLabel("Your letter is: " + letter, alignment=QtCore.Qt.AlignCenter)
        self.backButton = QtWidgets.QPushButton("Back")
        self.laying = QtWidgets.QVBoxLayout(self)
        self.laying.addWidget(self.letter) 
        self.laying.addWidget(self.text)
        self.laying.addWidget(self.backButton)
        self.backButton.clicked.connect(lambda: controller.setPage(0))
class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.stack = QtWidgets.QStackedWidget()
        self.home = homeMenu(self)
        self.comms = commMenu(self, False, 'A')
        self.stack.addWidget(self.home)
        self.stack.addWidget(self.comms)
        self.setCentralWidget(self.stack)
        self.stack.setCurrentIndex(0)
    def setPage(self, index: int, pieceTypeIn = False, letterIn = ''):
        self.comms = commMenu(self, pieceTypeIn, letterIn)
        self.stack.setCurrentIndex(index)

        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()
