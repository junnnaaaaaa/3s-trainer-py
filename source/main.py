import sys
import random
import string
import datahandling as data
from PySide6 import QtCore, QtWidgets, QtGui

LETTERS = [chr(i) for i in range(65, 89)]
class letterDialogue(QtWidgets.QDialog):
    def __init__(self, controller):
        super().__init__()
        self.setFixedSize(400,400)
        self.setWindowTitle("Enter first letter:")
        self.prompt = QtWidgets.QLabel("Enter first letter of letter pair:")
        self.edit = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("Enter")
        self.laying = QtWidgets.QVBoxLayout()
        self.laying.addWidget(self.prompt)
        self.laying.addWidget(self.edit)
        self.laying.addWidget(self.button)
        self.setLayout(self.laying)
        self.button.clicked.connect(lambda: self.enter(controller))
        self.pieceType = False
        self.firstLetter = ''
    def iniate(self, pieceTypeIn = False):
        self.show()
        self.pieceType = pieceTypeIn
        return

    def enter(self, controller):
        self.firstLetter = self.edit.text().capitalize()
        if self.firstLetter in LETTERS:
            controller.setPage(1,  self.pieceType, self.firstLetter )
            self.close()
        else:
            QtWidgets.QMessageBox.about(self, 'Error','Input can only be a letter between A and X')
        return


class letterPair(QtWidgets.QWidget):
    def __init__(self, controller, letter1: str, letter2: str):
        super().__init__() 
        self.setMaximumSize(380, 100)
        self.setMinimumSize(200, 100) 
        self.laying = QtWidgets.QVBoxLayout(self)
        self.laying.setSpacing(1)
        self.laying.setAlignment(QtCore.Qt.AlignTop)
        if letter1 == letter2:
            self.button = QtWidgets.QPushButton("Placeholder")
            self.laying.addWidget(self.button)
        else:
            self.pieceType = controller.pieceType  
            self.letters = letter1+letter2
            self.toggleState = False
            self.comm = data.fetchPair(letter1+letter2, controller.pieceType)[0]
            self.word = data.fetchPair(letter1+letter2, controller.pieceType)[1]
            self.commEnter = QtWidgets.QLineEdit(self.comm)
            self.commEnter.setPlaceholderText("Enter your commutator")
            self.wordEnter =  QtWidgets.QLineEdit(self.word)
            self.wordEnter.setPlaceholderText("Enter your word")
            self.enterButton = QtWidgets.QPushButton("Enter")
            self.button = QtWidgets.QPushButton(letter1+letter2)
            self.laying.addWidget(self.button)
            self.button.clicked.connect(lambda: self.toggle())
            self.enterButton.clicked.connect(lambda: self.enter())

    def verify(self, comm):
        #Placeholder function for verification purposes
        return True
    def toggle(self):
        if not self.toggleState:
            self.toggleState = True
            self.laying.addWidget(self.commEnter)
            self.laying.addWidget(self.wordEnter)
            self.laying.addWidget(self.enterButton)
            self.commEnter.show()
            self.wordEnter.show()
            self.enterButton.show()
        else:    
            self.toggleState = False
            self.laying.removeWidget(self.commEnter)
            self.laying.removeWidget(self.wordEnter)
            self.laying.removeWidget(self.enterButton)
            self.commEnter.hide()
            self.wordEnter.hide()
            self.enterButton.hide()

    def enter(self):
        if self.verify(self.commEnter.text()):
            self.comm= self.commEnter.text()
            self.word= self.wordEnter.text() 
            data.addPair(self.pieceType, self.letters, self.comm, self.word)
            self.laying.removeWidget(self.commEnter)
            self.laying.removeWidget(self.wordEnter)
            self.laying.removeWidget(self.enterButton)
            self.commEnter.hide()
            self.wordEnter.hide()
            self.enterButton.hide()
            self.toggleState = False
        else:
            QtWidgets.QMessageBox.about(self, "Error", "Commutator entered is not valid")

class homeMenu(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.laying = QtWidgets.QVBoxLayout(self)
        self.edgeButton = QtWidgets.QPushButton("Edge Menu")
        self.cornerButton = QtWidgets.QPushButton("Corner Menu")
        self.text = QtWidgets.QLabel("Main Menu", alignment=QtCore.Qt.AlignCenter)
        self.laying.addWidget(self.text)
        self.laying.addWidget(self.edgeButton)
        self.laying.addWidget(self.cornerButton)
        self.edgeButton.clicked.connect(lambda: controller.dialog.iniate(True))
        self.cornerButton.clicked.connect(lambda: controller.dialog.iniate(False))
class commMenu(QtWidgets.QWidget):
    def __init__(self, controller, pieceType: bool, letter: str):
        super().__init__()
        self.pieceType = pieceType
        self.text = QtWidgets.QLabel(
            ("Edge Menu: " if self.pieceType else "Corner Menu: ") + letter,
            alignment=QtCore.Qt.AlignCenter,
        )
        self.backButton = QtWidgets.QPushButton("Back")
        self.laying = QtWidgets.QGridLayout(self)
        self.laying.addWidget(self.text, 0, 0, 3, 0)
        self.backButton.clicked.connect(lambda: controller.setPage(0))
        self.pairButtons = []
        self.laying.setSpacing(5)
        self.grid = QtWidgets.QWidget()
        self.grid.setLayout(self.laying)
        self.outer = QtWidgets.QHBoxLayout(self)
        self.outer.addStretch()
        self.outer.addWidget(self.grid)
        self.outer.addStretch() 
    
        for i in range(len(LETTERS)):
            self.pairButtons.append(letterPair(self, letter, LETTERS[i]))
            if i < 4:
                self.laying.addWidget(self.pairButtons[i], 2, i)
            else:
                self.laying.addWidget(self.pairButtons[i])
        self.laying.addWidget(self.backButton, 8, 0)





class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3 Style trainer")
        self.stack = QtWidgets.QStackedWidget()
        self.home = homeMenu(self)
        self.comms = commMenu(self, False, "A")
        self.stack.addWidget(self.home)
        self.stack.addWidget(self.comms)
        self.setCentralWidget(self.stack)
        self.dialog = letterDialogue(self)
        self.stack.setCurrentIndex(0)
        self.pieceType = False
        importEdgeWords = QtGui.QAction("Import Edges",self)
        importCornerWords = QtGui.QAction("Import Corners",self)       
        importEdgeComm = QtGui.QAction("Import Edges",self)
        importCornerComm = QtGui.QAction("Import Corners",self) 
        clearComms = QtGui.QAction("Clear Comms",self)
        clearComms.triggered.connect(lambda: self.clearData("commutator"))
        clearWords = QtGui.QAction("Clear Words",self)
        clearWords.triggered.connect(lambda: self.clearData("word"))
        menu = self.menuBar()
        fileMenu = menu.addMenu("&File")
        fileWords= fileMenu.addMenu("Import Words")
        fileWords.addAction(importEdgeWords)
        fileWords.addAction(importCornerWords)
        fileComms= fileMenu.addMenu("Import Comms")
        fileComms.addAction(importEdgeComm)
        fileComms.addAction(importCornerComm)
        fileClear = fileMenu.addMenu("Clear data")
        fileClear.addAction(clearComms)
        fileClear.addAction(clearWords)
    def importData(self, pieceTypeIn, dataType):
        #placeholder for file part
        return
    def clearData(self, dataType):
        self.confirmBox = QtWidgets.QMessageBox()
        self.confirmBox.setText("Warning: All data will be cleared and not saved")
        self.confirmBox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Apply | QtWidgets.QMessageBox.StandardButton.Cancel)
        self.confirmBox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
        self.apply = self.confirmBox.exec()
        if self.apply == QtWidgets.QMessageBox.StandardButton.Apply:
            data.resetPairs(dataType)
            self.setPage(0)  
    def setPage(self, index: int, pieceTypeIn=False, letterIn=''):
        self.stack.removeWidget(self.comms)
        if index == 1:
            self.comms = commMenu(self, pieceTypeIn, letterIn)
        self.stack.addWidget(self.comms)
        self.stack.setCurrentIndex(index)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet("""
    QPushButton {
        font-size: 14px;
    }
    QLabel {
        font-size: 18px;
        padding:5px;
    }
    QLineEdit {
        font-size: 12px;
        padding: 3px;
    }
""")
    data.initiatePairs()
    window = mainWindow()
    window.show()
    app.exec()
