from PyQt6.QtPrintSupport import QPrintDialog
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDockWidget, QPushButton, QVBoxLayout, \
    QLabel, QMessageBox, QHBoxLayout, QLCDNumber, QDialog, QInputDialog
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap
import sys, csv, random
from PyQt6.QtCore import Qt, QPoint, QTimer


class PictionaryGame(QMainWindow):

    '''Painting Application class'''
    def __init__(self):
        super().__init__()

        self.gameSet = False
        self.initUi()

        """centers the window"""
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUi(self):
        self.setWindowTitle("Pictionary Game")  # set window title
        self.setGeometry(400, 400, 800, 600)  # set the windows dimensions
        self.setWindowIcon(QIcon("./icons/paint-brush.png")) #sets the icon

        # image settings (default)
        self.image = QPixmap("./icons/canvas.png")
        self.image.fill(Qt.GlobalColor.white)
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()

        '''Toolbar and items for it'''
        self.lvl = QAction('Level: Easy', self)
        self.lvl.setShortcut('Ctrl+L')
        self.lvl.triggered.connect(self.difficulty)

        self.tmr = QAction('Timer: 30s', self)
        self.tmr.setShortcut('Ctrl+T')
        self.tmr.triggered.connect(self.timer)

        self.plrs = QAction('Players: 2', self)
        self.plrs.setShortcut('Ctrl+P')
        self.plrs.triggered.connect(self.players)

        self.toolbar = self.addToolBar('Level')
        self.toolbar.addAction(self.lvl)
        self.toolbar.addAction(self.tmr)
        self.toolbar.addAction(self.plrs)

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(" File")  # add the file menu to the menu bar
        brushSizeMenu = mainMenu.addMenu(" Brush Size")  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(" Brush Colour")  # add the "Brush Colour" menu to the menu bar
        helpMenu = mainMenu.addMenu(" Help")  # add the "Help" menu to the menu bar

        # open menu item
        openAction = QAction(QIcon("./icons/file_icons/open.png"), "Open", self)  # create a open action with a png as an icon
        openAction.setShortcut("Ctrl+O")  # connect this open action to a keyboard shortcut
        fileMenu.addAction(openAction)  # add the save action to the file menu
        openAction.triggered.connect(self.open)  # when the menu option is selected or the shortcut is used the open slot is triggered

        # save menu item
        saveAction = QAction(QIcon("./icons/file_icons/save.png"), "Save", self)  # create a save action with a png as an icon
        saveAction.setShortcut("Ctrl+S")  # connect this save action to a keyboard shortcut
        fileMenu.addAction(saveAction)  # add the save action to the file menu
        saveAction.triggered.connect(self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered

        # clear
        clearAction = QAction(QIcon("./icons/file_icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # reset
        resetAction = QAction(QIcon("./icons/file_icons/reset.png"), "Reset Game", self)  # create a clear action with a png as an icon
        resetAction.setShortcut("Ctrl+L")  # connect this reset action to a keyboard shortcut
        fileMenu.addAction(resetAction)  # add this action to the file menu
        resetAction.triggered.connect(self.reset)  # when the menu option is selected or the shortcut is used the reset slot is triggered

        # close the app
        exitAction = QAction(QIcon("./icons/file_icons/exit.png"), "Exit", self)  # create a close action with a png as an icon
        exitAction.setShortcut("Ctrl+Q")  # connect this save action to a keyboard shortcut
        fileMenu.addAction(exitAction)  # add the close action to the file menu
        exitAction.triggered.connect(self.close)  # when the menu option is selected or the shortcut is used the close slot is triggered

        # brush thickness
        threepxAction = QAction(QIcon("./icons/brush_sizes/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/brush_sizes/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/brush_sizes/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/brush_sizes/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/colors/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction)
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/colors/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction)
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/colors/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction)
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/colors/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellow)

        # help menu items
        aboutAction = QAction(QIcon("./icons/help_icons/about.png"), "About", self)  # create a close action with a png as an icon
        aboutAction.setShortcut("Ctrl+A")  # connect this save action to a keyboard shortcut
        helpMenu.addAction(aboutAction)  # add the about action to the help menu
        aboutAction.triggered.connect(self.showAbout)  # when the menu option is selected or the shortcut is used the about slot is triggered

        helpAction = QAction(QIcon("./icons/help_icons/help.png"), "Help", self)  # create a close action with a png as an icon
        helpAction.setShortcut("Ctrl+H")  # connect this save action to a keyboard shortcut
        helpMenu.addAction(helpAction)  # add the help action to the help menu
        helpAction.triggered.connect(self.showHelp)  # when the menu option is selected or the shortcut is used the help slot is triggered

        # Side Dock
        self.dockInfo = QDockWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        #brush color and size info
        self.brColor = QPixmap("./icons/colors/black.png").scaled(15, 15, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.bColor = QLabel()
        self.bColor.setPixmap(self.brColor)
        self.brThicknessImg = QPixmap("./icons/brush_sizes/threepx.png")
        self.bThickLbl = QLabel()
        self.bThickLbl.setPixmap(self.brThicknessImg)
        self.brushThicknessVal = QLabel(str(self.brushSize))
        bsh = QHBoxLayout()
        bsh.addWidget(self.bColor)
        bsh.addWidget(QLabel(" "))
        bsh.addWidget(self.bThickLbl)
        bsh.addWidget(self.brushThicknessVal)
        bsh.addWidget(QLabel("px"))

        # timer widget
        self.timer = QLCDNumber()
        self.timer.setDigitCount(5)  # Format: "MM:SS"
        self.timer.display("00:30")

        # widget inside the Dock
        playerInfo = QWidget()
        self.vbdock = QVBoxLayout()
        playerInfo.setLayout(self.vbdock)
        playerInfo.setMaximumSize(100, self.height())

        # add controls to custom widget
        '''currrent turn'''
        self.players_turns = {}
        for i in range(1, 5): #dict for the players
            self.players_turns[f"p{i}"] = i
        self.vbdock.addWidget(QLabel("<b>Current Turn:</b>"))
        self.cturn = self.players_turns["p1"] #current player
        self.current_player = QLabel("Player "+str(self.cturn))
        self.vbdock.addWidget(self.current_player)
        self.vbdock.addSpacing(20)

        '''timer'''
        self.vbdock.addWidget(QLabel("<b>Timer:</b>"))
        self.vbdock.addWidget(self.timer)
        self.vbdock.addSpacing(20)

        '''brush settings'''
        self.vbdock.addWidget(QLabel("<b>Brush settings:</b>"))
        self.vbdock.addLayout(bsh)
        self.vbdock.addSpacing(20)

        '''scores'''
        self.vbdock.addWidget(QLabel("<b>Scores:</b>"))
        self.playerNumber = 2
        self.player_labels = {}  # Dictionary to store layouts for each player
        self.player_scores = {}  # Dictionary to store labels for each player
        self.player_scores_int = {}
        for i in range(1, 5): #populates the block with players according to the number of players
            phb = QHBoxLayout()
            score = 0
            if i <= self.playerNumber:
                player_label = QLabel(f"Player {i}:")
                phb.addWidget(player_label)
                player_score = QLabel(str(score))
                phb.addWidget(player_score)
            else:
                player_label = QLabel("")
                phb.addWidget(player_label)
                player_score = QLabel("")
                phb.addWidget(player_score)
            # Store layouts and labels in dictionaries with keys
            self.player_scores_int[f"p{i}"] = score
            self.player_labels[f"pl{i}"] = player_label
            self.player_scores[f"ps{i}"] = player_score
            self.vbdock.addLayout(phb) # Add the layout to the main layout (vbdock)
        self.vbdock.addSpacing(20)

        '''buttons for answers and skip turn/start'''
        self.vbdock.addStretch(1)
        answerLaber = QLabel("<b>Answer:</b>")
        self.vbdock.addWidget(answerLaber)
        self.player_buttons = {}
        for i in range(1, 5): #creates buttons for answers in a loop
            b = QPushButton(f"Player{i}")
            b.setStyleSheet("background-color: lightblue;")
            self.vbdock.addWidget(b)
            self.player_buttons[f"pb{i}"] = b
            b.setEnabled(False)
        self.player_buttons["pb1"].clicked.connect(lambda: self.wordInput(1))
        self.player_buttons["pb2"].clicked.connect(lambda: self.wordInput(2))
        self.player_buttons["pb3"].clicked.connect(lambda: self.wordInput(3))
        self.player_buttons["pb4"].clicked.connect(lambda: self.wordInput(4))
        self.vbdock.addSpacing(20)
        self.button = QPushButton("Start")
        self.button.setStyleSheet("background-color: lightgreen;")
        self.button.clicked.connect(self.setButton)
        self.vbdock.addWidget(self.button)

        # Sets timer
        self.timer_count = QTimer(self)
        self.timer_count.timeout.connect(self.timer_update)

        # Setting colour of dock to gray
        playerInfo.setAutoFillBackground(True)
        p = playerInfo.palette()
        p.setColor(playerInfo.backgroundRole(), Qt.GlobalColor.gray)
        playerInfo.setPalette(p)

        # set widget for dock
        self.dockInfo.setWidget(playerInfo)

        #easy mode as default
        self.getList("easy")
        self.currentWord = self.getWord()

    def change_turn(self):
        '''funt to change turns'''
        if self.cturn == self.playerNumber:
            self.cturn = 1
        else:
            self.cturn = self.cturn+1
        self.current_player.setText(f"Player {self.cturn}") #sets the current player

    def reset(self):
        self.getList("easy") #sets difficulty easy
        self.currentWord = self.getWord() #sets a new word
        self.lvl.setText("Level: Easy") #changes level

        self.timer.display("00:30") #resets timer
        self.timer_count.stop() #stops timer
        self.tmr.setText("Timer: 30s") #changes timer setting

        self.playerNumber = 2 #resets the player numbers
        for i in range(1, 5): #resets scores
            self.player_labels[f"pl{i}"].setText("")
            self.player_scores[f"ps{i}"].setText("")
        for i in range(1, self.playerNumber+1):
            self.player_labels[f"pl{i}"].setText(f"Player {i}:")
            self.player_scores[f"ps{i}"].setText("0")
        self.plrs.setText("Players: 2") #resets number of players setting

        self.button.setText("Start") #resets the button
        self.button.setStyleSheet("background-color: lightgreen;")

        self.clear() #clears the canvas

        #resets the brush settings
        self.threepx()
        self.black()

        for i in range(1, 5): #sets the answer buttons
            self.player_buttons[f"pb{i}"].setStyleSheet("background-color: lightblue;")
            self.player_buttons[f"pb{i}"].setEnabled(False)
        self.update() #updates the app

    def restart(self):#
        self.clear() #clears the canvas
        self.button.setText("Start") #resets the button
        self.update() #updates the ui

    def difficulty(self):
        #toggle the text and changes the mode
        if self.lvl.text() == "Level: Hard":
            self.getList("easy")
            self.currentWord = self.getWord()
            self.lvl.setText("Level: Easy")
        elif self.lvl.text() == "Level: Easy":
            self.getList("hard")
            self.currentWord = self.getWord()
            self.lvl.setText("Level: Hard")

    def timer(self):
        #changes the timer values according to the settings
        if self.tmr.text() == "Timer: 30s":
            self.timer.display("01:00")
            self.tmr.setText("Timer: 60s")
        elif self.tmr.text() == "Timer: 60s":
            self.timer.display("01:30")
            self.tmr.setText("Timer: 90s")
        elif self.tmr.text() == "Timer: 90s":
            self.timer.display("02:00")
            self.tmr.setText("Timer: 120s")
        elif self.tmr.text() == "Timer: 120s":
            self.timer.display("00:30")
            self.tmr.setText("Timer: 30s")

        self.timer_restart()
        #self.timer_count.stop()

    def players(self):
        #sets the player number (scores and buttons) according to the player number settings
        for i in range(1, self.playerNumber + 1): #disables all buttons
            self.player_buttons[f"pb{i}"].setEnabled(False)

        for i in range(1, 5): #resets the scores and labels
            self.player_labels[f"pl{i}"].setText("")
            self.player_scores[f"ps{i}"].setText("")

        #changes the player settings
        if self.plrs.text() == "Players: 2":
            self.playerNumber = 3
            self.plrs.setText("Players: 3")
        elif self.plrs.text() == "Players: 3":
            self.playerNumber = 4
            self.plrs.setText("Players: 4")
        elif self.plrs.text() == "Players: 4":
            self.playerNumber = 2
            self.plrs.setText("Players: 2")

        for i in range(1, self.playerNumber+1): #sets the actual number of scores according to the number of players
            self.player_labels[f"pl{i}"].setText(f"Player {i}:")
            self.player_scores[f"ps{i}"].setText("0")

        if self.button.text() == "Skip Turn": #if game is not started, sets the buttons
            for i in range(1, 5): #sets the buttons for the current number of players
                if i<=self.playerNumber:
                    self.player_buttons[f"pb{i}"].setStyleSheet("background-color: lightgreen;")
                    self.player_buttons[f"pb{i}"].setEnabled(True)
                else:
                    self.player_buttons[f"pb{i}"].setStyleSheet("background-color: lightblue;")

    def setButton(self):

        if self.button.text() == 'Start': #if the game wasnt started
            self.button.setText("Skip Turn") #changes the button text and color
            self.button.setStyleSheet("background-color: lightblue;")

            for i in range(1, self.playerNumber+1): #enables players buttons
                self.player_buttons[f"pb{i}"].setStyleSheet("background-color: lightgreen;")
                self.player_buttons[f"pb{i}"].setEnabled(True)

        elif self.button.text() == 'Skip Turn': #if skip turn is pressed
            self.difficulty() #sets the new word
            self.clear() #clears the canvas
            self.change_turn() #changes turn

        self.warning() #shows the message and the word

    def warning(self):
        '''shows the window with the warning before showing the word'''
        w = QDialog()
        w.setWindowIcon(QIcon("./icons/paint-brush.png"))
        w.setWindowTitle("Warning")
        t = QLabel(f"<b>All players</b> except <b>Player{self.cturn}</b> should close their eyes!")
        b = QPushButton("Done")
        b.clicked.connect(w.accept)
        b.clicked.connect(self.show_word)
        l = QVBoxLayout()
        l.addSpacing(20)
        l.addWidget(t)
        l.addSpacing(20)
        l.addWidget(b)
        w.setLayout(l)
        w.exec()

    def show_word(self):
        '''shows window with the word on the screen'''
        w = QDialog()
        w.setWindowIcon(QIcon("./icons/paint-brush.png"))
        w.setWindowTitle("Word")
        t = QLabel(f"The word to draw: <b>{self.currentWord}</b>")
        b = QPushButton("Ok")
        b.clicked.connect(w.accept)
        b.clicked.connect(self.timer_restart)
        l = QVBoxLayout()
        l.addSpacing(20)
        l.addWidget(t)
        l.addSpacing(20)
        l.addWidget(b)
        w.setLayout(l)
        w.exec()

    def wordInput(self, i: int):
        '''funtion to check the corecctness of the input word'''
        msg = 'Your Guess:'
        while True: #loop to open the window if the guess is wrong
            text, ok = QInputDialog.getText(self, 'Enter The Word', msg)
            if not ok:
                break
            self.guessWord = text
            if self.guessWord.lower() == self.currentWord.lower(): #if guess is right
                '''window that congfirms the right guess'''
                w = QDialog()
                w.setWindowIcon(QIcon("./icons/paint-brush.png"))
                w.setWindowTitle("Correct")
                w.setFixedWidth(200)
                t = QLabel("Right Answer")
                b = QPushButton("Ok")
                b.clicked.connect(w.accept)
                l = QVBoxLayout()
                l.addWidget(t)
                l.addWidget(b)
                w.setLayout(l)
                w.exec()
                '''adjusting the scores'''
                self.player_scores_int[f"p{i}"] = self.player_scores_int[f"p{i}"]+1
                self.player_scores[f"ps{i}"].setText(str(self.player_scores_int[f"p{i}"]))
                self.player_scores_int[f"p{self.cturn}"] = self.player_scores_int[f"p{self.cturn}"]+2
                self.player_scores[f"ps{self.cturn}"].setText(str(self.player_scores_int[f"p{self.cturn}"]))
                self.change_turn()
                self.timer_restart()
                self.difficulty()
                self.warning()
                break
            else:
                msg = 'Wrong Answer, try again:' #if guess is wrong

    def timer_update(self):
        '''function to update the timer values'''
        if not self.button.text() == "Skip Turn":
            self.button.setText("Skip Turn")

        if self.time_left > 0:
            self.time_left -= 1
            minutes = self.time_left // 60
            seconds = self.time_left % 60
            self.timer.display(f"{minutes:02}:{seconds:02}")
        else:
            self.timer_count.stop()
            self.timer.display("00:00")
            self.clear()
            self.change_turn()
            self.button.setStyleSheet("background-color: lightgreen;")
            self.button.setText("Start")

    def timer_restart(self):
        '''funct to sets the timer according to the setting'''
        if self.tmr.text() == "Timer: 30s":
            self.time_left = 30
            self.timer.display("00:30")

        elif self.tmr.text() == "Timer: 60s":
            self.time_left = 60
            self.timer.display("01:00")

        elif self.tmr.text() == "Timer: 90s":
            self.time_left = 90
            self.timer.display("01:30")

        elif self.tmr.text() == "Timer: 120s":
            self.time_left = 120
            self.timer.display("02:00")

        if self.button.text() == "Skip Turn":
            self.timer_count.start(1000)  # Start or restart the countdown

    def showAbout(self):
        # shows about window
        try: #reads the content of about file
            with open("help/about.txt", "r") as file:
                about_text = file.read()
        except FileNotFoundError:
            about_text = "Error: about.txt not found. /nReload the application or check the content integrity."
        #display the content
        QMessageBox.information(self, "About", about_text)

    def showHelp(self):
        # shows help window
        try: #reads the content of help file
            with open("help/help.txt", "r") as file:
                help_text = file.read()
        except FileNotFoundError:
            help_text = "Error: help.txt not found. /nReload the application or check the content integrity."
        #display the content
        QMessageBox.information(self, "Help", help_text)

    # event handlers
    def mousePressEvent(self, event):  # when the mouse is pressed, documentation: https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
            print(self.lastPoint)  # print the lastPoint for debugging purposes

    def mouseMoveEvent(self, event):  # when the mouse is moved, documenation: documentation: https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here http://doc.qt.io/qt-6/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())  # draw a line from the point of the orginal press to the point to where the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to, this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self, event):  # when the mouse is released, documentation: https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button, documentation: https://doc.qt.io/qt-6/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(self)  # create a new QPainter object, documentation: https://doc.qt.io/qt-6/qpainter.html
        canvasPainter.drawPixmap(QPoint(), self.image)  # draw the image , documentation: https://doc.qt.io/qt-6/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # slots
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(
            Qt.GlobalColor.white)  # fill the image with white, documentation: https://doc.qt.io/qt-6/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    def brush_info_update(self):
        '''updates brush info on the left side window'''
        self.brushThicknessVal.setText(str(self.brushSize))
        self.bColor.setPixmap(self.brColor)
        self.bThickLbl.setPixmap(self.brThicknessImg)

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3
        self.brThicknessImg = QPixmap("./icons/brush_sizes/threepx.png")
        self.brush_info_update()

    def fivepx(self):
        self.brushSize = 5
        self.brThicknessImg = QPixmap("./icons/brush_sizes/fivepx.png")
        self.brush_info_update()

    def sevenpx(self):
        self.brushSize = 7
        self.brThicknessImg = QPixmap("./icons/brush_sizes/sevenpx.png")
        self.brush_info_update()

    def ninepx(self):
        self.brushSize = 9
        self.brThicknessImg = QPixmap("./icons/brush_sizes/ninepx.png")
        self.brush_info_update()

    def black(self):  # the brush color is set to black
        self.brushColor = Qt.GlobalColor.black
        self.brColor = QPixmap("./icons/colors/black.png").scaled(15, 15, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.brush_info_update()

    def red(self):
        self.brushColor = Qt.GlobalColor.red
        self.brColor = QPixmap("./icons/colors/red.png").scaled(15, 15, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.brush_info_update()

    def green(self):
        self.brushColor = Qt.GlobalColor.green
        self.brColor = QPixmap("./icons/colors/green.png").scaled(15, 15, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.brush_info_update()

    def yellow(self):
        self.brushColor = Qt.GlobalColor.yellow
        self.brColor = QPixmap("./icons/colors/yellow.png").scaled(15, 15, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.brush_info_update()

    #Get a random word from the list read from file
    def getWord(self):
        self.randomWord = random.choice(self.wordList)
        print(self.randomWord)
        return self.randomWord

    #read word list from file
    def getList(self, mode):
        with open(mode + 'mode.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                #print(row)
                self.wordList = row
                line_count += 1
            #print(f'Processed {line_count} lines.')

    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file dialog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class

# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PictionaryGame()
    window.show()
    app.exec()  # start the event loop running
