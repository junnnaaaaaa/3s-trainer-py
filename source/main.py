import sys
import random
import string
from PySide6 import QtCore, QtWidgets, QtGui
LETTERS = [chr(i) for i in range(65, 89)]
class letterDialogue(QtWidgets.QDialog):
    def __init__(self, controller):
        super().__init__()
        self.edit = QtWidgets.QLineEdit("Enter first letter:")
        self.button = QtWidgets.QPushButton("Enter")
        self.laying = QtWidgets.QVBoxLayout()
        self.laying.addWidget(self.edit)
        self.laying.addWidget(self.button)
        self.setLayout(self.laying)
        self.button.clicked.connect(self.enter(controller))
        self.firstLetter = ''
    def enter(self, controller):
        self.firstLetter = self.edit.text()
        controller.comms = commMenu(self, False, self.firstLetter)
        controller.stack.addWidget(controller.comms())
        self.close()
        return
class letterPair(QtWidgets.QPushButton):
    def __init__(self, controller, letter1: str, letter2: str):
        super().__init__(letter1+letter2)
        self.comm = ''
        # self.menu = QtWidgets.QTabWidget()
class homeMenu(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.laying = QtWidgets.QVBoxLayout(self)
        self.edgeButton = QtWidgets.QPushButton("Edge Menu")
        self.cornerButton = QtWidgets.QPushButton("Corner Menu")
        self.text = QtWidgets.QLabel("Main Menu",
                                     alignment=QtCore.Qt.AlignCenter)
        self.laying.addWidget(self.text)
        self.laying.addWidget(self.edgeButton)
        self.laying.addWidget(self.cornerButton)
        self.edgeButton.clicked.connect(lambda: controller.setPage(1, True, True))
        self.cornerButton.clicked.connect(lambda: controller.setPage(1, False, True))
class commMenu(QtWidgets.QWidget):
    def __init__(self, controller, pieceType: bool, letter: str):
        super().__init__()
        self.text = QtWidgets.QLabel(( "Edge Menu: " if pieceType else "Corner Menu: ") + letter,
                                     alignment=QtCore.Qt.AlignCenter)
        self.backButton = QtWidgets.QPushButton("Back")
        self.laying = QtWidgets.QVBoxLayout(self)
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
        self.dialog = letterDialogue(self)
        self.stack.setCurrentIndex(0)
    def setPage(self, index: int, pieceTypeIn = False, letterIn = False):
        if letterIn:
            self.stack.removeWidget(self.comms)
            self.dialog.show()
        else:
            self.stack.setCurrentIndex(index)

        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mainWindow()
    window.show()
    app.exec()
