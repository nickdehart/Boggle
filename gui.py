"""Nicholas DeHart"""

import sys, shelve
from PyQt5 import QtWidgets, QtCore, QtGui
from boggle import Boggle

class BoggleWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        new = QtWidgets.QAction('&New', self)
        new.setShortcut("Ctrl+N")
        new.triggered.connect(self.new_game)
        save = QtWidgets.QAction("&Save", self)
        save.setShortcut("Ctrl+S")
        save.triggered.connect(self.save_game)
        load = QtWidgets.QAction("&Load", self)
        load.setShortcut("Ctrl+L")
        load.triggered.connect(self.load_game)
        
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        game_menu = menu_bar.addMenu('Game')
        game_menu.addAction(new)
        game_menu.addAction(save)
        game_menu.addAction(load)

        self.loading = []
        reply = StartMessage(self).exec_()
        if reply == 0:
            self.setup()
        else:
            self.load_game()

    def setup(self):
        self.setWindowTitle('boggle.py')
        self.setFixedSize(800, 400)
        
        self.game = Game(self, self.loading)
        self.setCentralWidget(self.game)

        self.show()

    def new_game(self):
        self.setup()

    def save_game(self):
        """1. Saving and restoring the dice configuration. 
        2. Saving and restoring the words already entered (i.e. the ones in the right text box)
        3. Saving and restoring the time left on the clock. """
        saveStamp = self.loading[0]
        saveDice = self.loading[1]
        saveWords = self.loading[2]
        saveTime = self.loading[3]

    def load_game(self):
        load = LoadMessage(self).exec_()

class Game(QtWidgets.QWidget):
    def __init__(self, parent, loading):
        QtWidgets.QWidget.__init__(self, parent)
        self.setup(parent, loading)
    
    def setup(self, parent, loading):
        self.parent = parent
        self.answers = []
        self.board = DiceGrid(self, loading) 
        self.words = QtWidgets.QTextEdit()
        self.words.setReadOnly(True)
        self.wordInput = QtWidgets.QLineEdit()
        self.wordInput.editingFinished.connect(self.enterPress)
        self.seconds = 180
        self.time = QtWidgets.QLCDNumber()
        self.time.display(self.seconds)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
    
        self.grid.addWidget(self.board,0,0)
        self.grid.addWidget(self.words,0,1)
        self.grid.addWidget(self.wordInput,1,0)
        self.grid.addWidget(self.time,1,1)

    def enterPress(self):
        self.words.append(self.wordInput.text())
        self.board.boggle.answers.append(self.wordInput.text())
        self.wordInput.clear()

    def update(self):
        if self.seconds > 1:
            self.seconds -= 1
            self.time.display(self.seconds)
        else:
            self.wordInput.setReadOnly(True)
            reply = QuitMessage(self).exec_()
            if reply == QtWidgets.QMessageBox.No:
                QtWidgets.qApp.quit()
            elif reply == QtWidgets.QMessageBox.Yes:
                self.parent.setup()

class DiceGrid(QtWidgets.QWidget):
    def __init__(self, parent, loading):
        QtWidgets.QWidget.__init__(self, parent)
        self.boggle = Boggle()
        if loading:
            self.boggle.boggleBoard = loading
        self.setup()
    
    def setup(self):
        layout = QtWidgets.QGridLayout()

        index =0
        for col in range(0,4):
            for row in range(0,4):
                die = QtWidgets.QLabel()
                die.setText(self.boggle.boggleBoard[index])
                index += 1
                newfont = QtGui.QFont("Arial", 18, QtGui.QFont.Bold) 
                die.setFont(newfont)
                die.setAlignment(QtCore.Qt.AlignCenter)
                die.setFrameStyle(QtWidgets.QFrame.Panel)
                layout.addWidget(die, col, row, 1, 1)
 
        self.setLayout(layout)

class StartMessage(QtWidgets.QMessageBox):
    def __init__(self, parent):
        QtWidgets.QMessageBox.__init__(self, parent)
        self.setText("Would you like to start a new game\nor load a saved game?")
        self.setWindowTitle("boggle.py")
        self.addButton(QtWidgets.QPushButton('Start New Game'), QtWidgets.QMessageBox.NoRole)
        self.addButton(QtWidgets.QPushButton('Load Game'), QtWidgets.QMessageBox.YesRole)

class LoadMessage(QtWidgets.QDialog):
    """1. Saving and restoring the dice configuration. 
    2. Saving and restoring the words already entered (i.e. the ones in the right text box)
    3. Saving and restoring the time left on the clock. """
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        label = QtWidgets.QLabel("Select a game to load:", self)
        label.move(5,5)
        loadList = QtWidgets.QListWidget(self)
        loadList.setFixedSize(290, 270)
        if parent.loading:
            for timestamp in parent.loading[0]:
                loadList.addItem(timestamp)
        loadList.move(5, 25)
        self.setWindowTitle("boggle.py")
        self.setFixedSize(300, 300)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

class QuitMessage(QtWidgets.QMessageBox):
    def __init__(self, parent):
        QtWidgets.QMessageBox.__init__(self, parent)
        parent.board.boggle.score_game()
        endingText = "Time's Up!\nScore: " + str(parent.board.boggle.score) + "\nWould you like to play again?"
        self.setText(endingText)
        self.setWindowTitle("boggle.py")
        self.addButton(self.No)
        self.addButton(self.Yes)

if __name__ == "__main__":
    boggle = QtWidgets.QApplication(sys.argv)
    main_window = BoggleWindow()
    boggle.exec_()