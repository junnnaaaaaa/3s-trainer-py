import sys
import random
import string
import random
import datahandling as data
import cubehandling as cube
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path
LETTERS = [chr(i) for i in range(65, 89)]
class NoKeyButton(QtWidgets.QPushButton):
    def keyPressEvent(self, event):
        event.ignore() 
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
            controller.setPage(2,  self.pieceType, self.firstLetter )
            self.close()
        else:
            QtWidgets.QMessageBox.about(self, 'Error','Input can only be a letter between A and X')
        return


class timer(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.msElapsed = 0
        self.running = False
        self.chosenPairs = []
        self.sessionTimes = []
        self.isEdge = True
        self.prompt = QtWidgets.QLabel("Your Pair and word will go here", alignment=QtCore.Qt.AlignCenter)
        self.pieceButton = NoKeyButton("Mode: edges")
        self.pieceButton.clicked.connect(lambda: self.pieceSwap())
        self.pairSelection = NoKeyButton("Select letter Pairs")
        self.pairSelection.clicked.connect(lambda: self.pairSelect.show())
        self.backButton = NoKeyButton("Back")
        self.backButton.clicked.connect(lambda: controller.setPage(0))
        self.timerDisplay = QtWidgets.QLabel("0.00")
        self.timerDisplay.setStyleSheet("font-size: 36pt;")
        self.timerDisplay.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        self.stats = QtWidgets.QLabel("Session stats:\nCurrent time:\nSession mean: ")
        self.pairSelect = QtWidgets.QDialog()
        self.pairSelect.setFixedSize(400,400)
        self.pairEnter = QtWidgets.QLineEdit()
        self.pairEnterButton = QtWidgets.QPushButton("Enter")
        self.pairEnterButton.clicked.connect(lambda: self.enterPair())
        self.pairEnter.setPlaceholderText("Enter your pairs")
        self.dialogLabel = QtWidgets.QLabel("Enter in pairs, or for set of pairs, just the first letter, separated by a comma and space. e.g.: 'A, BC, GH'")
        self.dialogLabel.setStyleSheet("font-size: 12pt")
        self.dialogLabel.setWordWrap(True)
        self.laying = QtWidgets.QVBoxLayout()   
        self.dialogLaying = QtWidgets.QVBoxLayout()   
        self.setLayout(self.laying)
        self.pairSelect.setLayout(self.dialogLaying)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.tick)
        self.laying.addWidget(self.prompt)
        self.laying.addWidget(self.timerDisplay)
        self.laying.addWidget(self.stats)
        self.laying.addWidget(self.pieceButton)
        self.laying.addWidget(self.pairSelection)
        self.laying.addWidget(self.backButton)
        self.dialogLaying.addWidget(self.dialogLabel)
        self.dialogLaying.addWidget(self.pairEnter)
        self.dialogLaying.addWidget(self.pairEnterButton)
    def pieceSwap(self):
        self.isEdge = not self.isEdge
        self.pieceButton.setText("Mode: " + data.strPiece(self.isEdge))
    def enterPair(self):
        allPairs = []
        try:
            self.chosenPairs = self.pairEnter.text().split(", ")
            for i in self.chosenPairs:
                i = i.upper()
                if len(i) == 1:
                    if i not in LETTERS:
                        QtWidgets.QMessageBox.about(self, 'Error','Formatting not valid')
                    else:
                        for j in LETTERS:
                            allPairs.append(i + j)
                elif len(i) == 2:
                    if i[0] not in LETTERS or i[1] not in LETTERS:
                        print(i)
                        QtWidgets.QMessageBox.about(self, 'Error','Formatting not valid')
                    else:
                        allPairs.append(i)
                else:
                    QtWidgets.QMessageBox.about(self, 'Error','Formatting not valid')
        except:
            QtWidgets.QMessageBox.about(self, 'Error','Formatting not valid')
        self.chosenPairs= allPairs
        print(self.chosenPairs)
        self.pairSelect.close()

    def tick(self):
        self.msElapsed += 10
        self.timerUpdate(self.msElapsed)
    def timerUpdate(self, ms):
        seconds = ms / 1000
        self.timerDisplay.setText(f"{seconds: .2f}")
    def keyReleaseEvent(self, event: QtGui.QKeyEvent):
         if event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat():
            if not self.running: 
                self.msElapsed = 0
                if self.chosenPairs:
                    self.chosenPair = random.choice(self.chosenPairs)
                    self.pairInfo = data.fetchPair(self.chosenPair, self.isEdge)
                    self.prompt.setText(f"Word: {self.pairInfo[1]}  Pair: {self.chosenPair}")
                self.running = True
                self.timer.start()
                self.timerDisplay.setStyleSheet("color: green; font-size: 36pt;")
            else:
                self.running = False
                self.timer.stop()
                self.timerDisplay.setStyleSheet("color: black; font-size: 36pt;")
                self.sessionTimes.append(self.msElapsed / 1000)
                self.stats.setText(f"Session stats:\nCurrent time: {self.sessionTimes[-1]} \nSession mean: {(sum(self.sessionTimes)/len(self.sessionTimes)): .2f} ")
         else:
            super().keyReleaseEvent(event)
    def keyPressEvent(self, event: QtGui.QKeyEvent):
         if event.key() == QtCore.Qt.Key_Space and not event.isAutoRepeat():
            self.timerDisplay.setStyleSheet("color: green; font-size: 36pt;")
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
        if cube.verifyAlg(self.commEnter.text()):
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
        self.timerButton = QtWidgets.QPushButton("Timer")
        self.edgeButton = QtWidgets.QPushButton("Edge Menu")
        self.cornerButton = QtWidgets.QPushButton("Corner Menu")
        self.text = QtWidgets.QLabel("Main Menu", alignment=QtCore.Qt.AlignCenter)
        self.laying.addWidget(self.text)
        self.laying.addWidget(self.timerButton)
        self.laying.addWidget(self.edgeButton)
        self.laying.addWidget(self.cornerButton)
        self.timerButton.clicked.connect(lambda: controller.setPage(1))
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
        self.timer = timer(self)
        self.stack.addWidget(self.home)
        self.stack.addWidget(self.timer)
        self.stack.addWidget(self.comms)
        self.setCentralWidget(self.stack)
        self.dialog = letterDialogue(self)
        self.stack.setCurrentIndex(0)
        self.pieceType = False
        importEdgeWords = QtGui.QAction("Import Edges",self)
        importCornerWords = QtGui.QAction("Import Corners",self)       
        importEdgeComm = QtGui.QAction("Import Edges",self)
        importCornerComm = QtGui.QAction("Import Corners",self) 
        importEdgeWords.triggered.connect(lambda: self.importData(True, "word"))
        importCornerWords.triggered.connect(lambda: self.importData(False, "word"))
        importEdgeComm.triggered.connect(lambda: self.importData(True, "commutator"))
        importCornerComm.triggered.connect(lambda: self.importData(False, "commutator"))
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
        filePath = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open File"), str(Path.home()), self.tr("CSV Files (*.csv)"))
        print("selection done")
        print(filePath)
        if not filePath[0] == '':
            print("import started")
            importOutput = data.importCsv(filePath[0], pieceTypeIn, dataType)
            if importOutput == "Bad table":
                QtWidgets.QMessageBox.about(self, "Import failed", "Please make sure your data is 25 by 25 with the first row and column being labels")
            else:
                QtWidgets.QMessageBox.about(self, "Import success", "The following pairs didn't import due to invalid comms/algs: " + importOutput)
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
        if index == 2:
            self.stack.removeWidget(self.comms)
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
