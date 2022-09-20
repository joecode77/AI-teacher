from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QToolBar, QAction, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QMovie, QIcon
import sounddevice as sd
import soundfile as sf
import datetime
import sys
#####################################################################################################################
from pyqtgraph.Qt import QtWidgets, QtCore
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import numpy as np
import pyaudio
import struct
######################################################################################################################
from AI.artificialIntelligence import Speak, Dictionary, Wikipedia, GoogleSearch
import AI.artificialIntelligence
import wikipedia
#######################################################################################################################
from Board.board import Window
from Dictionary.dictionary_search import DictionaryWindow
from Quiz.quiz_home import QuizWindow

class Worker(QThread):
    finished = pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        global playing
        hour = datetime.datetime.now().hour
        if hour < 12:
            data, fs = sf.read("audio/good morning.wav")
            sd.play(data, fs)
            sd.wait()
            AI.artificialIntelligence.playing = False
            # self.finished.emit()
        elif hour >= 12 and hour < 16:
            data, fs = sf.read("audio/good afternoon.wav")
            sd.play(data, fs)
            sd.wait()
            AI.artificialIntelligence.playing = False
        else:
            data, fs = sf.read("audio/good evening.wav")
            sd.play(data, fs)
            sd.wait()
            AI.artificialIntelligence.playing = False
            
    
class SoundWaves(QThread):
    def __init__(self, graphicsView):
        super().__init__()
        self.graphicsView = graphicsView

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 2

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )

    def run(self):
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        # waveform x points
        self.x = np.arange(0, 2 * self.CHUNK, 2)


    def plotGraph(self):
        wf_data = self.stream.read(self.CHUNK)
        wf_data = struct.unpack(str(2 * self.CHUNK) + 'B', wf_data)
        wf_data = np.array(wf_data, dtype='b')[::2] + 128
        self.graphicsView.clear()

        self.graphicsView.resize(700, 150)

        self.graphicsView.getAxis('left').setTextPen('black')
        self.graphicsView.getAxis('left').setPen('black')
        self.graphicsView.getAxis('bottom').setTextPen('black')
        self.graphicsView.getAxis('bottom').setPen('black')


        if AI.artificialIntelligence.playing == True:
            self.graphicsView.plot(self.x, wf_data, pen = "#ff0098")
        else:
            self.graphicsView.plot(self.x, wf_data, pen = "black")
        # pen = "#ff00ff"

class ClassRoom(QMainWindow):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.speak_icon = "icons/voice_muted.png"
        self.createWidgets()
        self.createLayouts()
        self.setWindowTitle("Socrates")
        self.setStyleSheet("background-color:#000000;color:white;")
        self.artificialIntelligenceAction()
        

    def createWidgets(self):

        self.empty_action1 = QAction()
        self.empty_action1.setEnabled(False)

        self.blackboard = QAction(QIcon("icons/blackboard.png"), "Blackboard")
        self.blackboard.triggered.connect(self.openBoard)
        self.blackboard.setStatusTip("Blackboard")

        self.empty_action2 = QAction()
        self.empty_action2.setEnabled(False)

        self.quiz = QAction(QIcon("icons/quiz.png"), "Quiz")
        self.quiz.triggered.connect(self.openQuiz)
        self.quiz.setStatusTip("Quiz")

        self.empty_action3 = QAction()
        self.empty_action3.setEnabled(False)

        self.chat = QAction(QIcon("icons/chat.png"), "Discussion Rooms")
        self.chat.setStatusTip("Discussion Rooms")

        self.empty_action4 = QAction()
        self.empty_action4.setEnabled(False)

        self.quote = QAction(QIcon("icons/quote.png"), "Educational Quotes")
        self.quote.setStatusTip(("Educational Quotes"))

        self.empty_action5 = QAction()
        self.empty_action5.setEnabled(False)

        self.contribution = QAction(QIcon("icons/contribution.png"), "Contribution")
        self.contribution.setStatusTip(("Contribution"))

        self.empty_action6 = QAction()
        self.empty_action6.setEnabled(False)

        self.dictionary = QAction(QIcon("icons/dictionary.png"), "Dictionary")
        self.dictionary.triggered.connect(self.openDictionary)
        self.dictionary.setStatusTip(("Dictionary"))

        self.empty_action7 = QAction()
        self.empty_action7.setEnabled(False)

        self.games = QAction(QIcon("icons/games.png"), "Games")
        self.games.setStatusTip(("Games"))

        self.empty_action8 = QAction()
        self.empty_action8.setEnabled(False)

        self.about = QAction(QIcon("icons/info.png"), "About")
        self.about.setStatusTip(("About"))

        tool_bar = QToolBar("Tools")

        tool_bar.addAction(self.empty_action1)
        tool_bar.addAction(self.blackboard)
        tool_bar.addAction(self.empty_action2)
        tool_bar.addAction(self.quiz)
        tool_bar.addAction(self.empty_action3)
        tool_bar.addAction(self.chat)
        tool_bar.addAction(self.empty_action4)
        tool_bar.addAction(self.quote)
        tool_bar.addAction(self.empty_action5)
        tool_bar.addAction(self.contribution)
        tool_bar.addAction(self.empty_action6)
        tool_bar.addAction(self.dictionary)
        tool_bar.addAction(self.empty_action7)
        tool_bar.addAction(self.games)
        tool_bar.addAction(self.empty_action8)
        tool_bar.addAction(self.about)

        tool_bar.setIconSize(QSize(50, 50))
        self.addToolBar(Qt.LeftToolBarArea, tool_bar)

        self.scifi_circle = QLabel()
        self.scifi_circle.setAlignment(Qt.AlignCenter)
        self.movie = QMovie("gifs/_ (1).gif")
        self.scifi_circle.setMovie(self.movie)
        self.movie.start()

        self.widget = QWidget()

        self.graphicsView = PlotWidget()
        # self.graphicsView.setGeometry(QtCore.QRect(10, 10, 200, 200))
        self.graphicsView.setObjectName("graphicsView")

        self.listening = QLabel()
        self.listening.setFont(QFont("Ariel, 20px"))
        self.listening.setStyleSheet("color:#ff0098;")

        self.speak = QPushButton()
        self.speak.setIcon(QIcon(self.speak_icon))
        self.speak.setStyleSheet("border:1px solid black;")
        self.speak.clicked.connect(self.getVoice)
        self.speak.setIconSize(QSize(100, 100))

        self.sound = SoundWaves(self.graphicsView)
        self.sound.start()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.sound.plotGraph)
        self.timer.start()

    def createLayouts(self):
        self.setCentralWidget(self.widget)
        
        self.layout = QVBoxLayout()
        self.audio_layout = QHBoxLayout()
        self.speak_layout = QHBoxLayout()
        
        
        self.layout.addStretch()


        self.layout.addWidget(self.scifi_circle)
        self.layout.addStretch(2)
        self.audio_layout.addStretch()
        self.layout.addLayout(self.audio_layout)
        self.audio_layout.addWidget(self.graphicsView)
        self.audio_layout.addStretch()
        self.layout.addStretch()
        self.layout.addStretch()
        self.layout.addWidget(self.listening)
        self.layout.addStretch()
        self.speak_layout.addStretch()
        self.layout.addLayout(self.speak_layout)
        self.speak_layout.addWidget(self.speak)
        self.speak_layout.addStretch()
        self.layout.addStretch()

        self.widget.setLayout(self.layout)

    def changeSpeakIcon(self):
        if "listening" in self.speak_icon:
            self.speak_icon = "icons/voice_muted.png"
            self.speak.setIcon(QIcon(self.speak_icon))
        else:
            self.speak_icon = "icons/voice_listening.png"
            self.speak.setIcon(QIcon(self.speak_icon))

    def getVoice(self):
        self.changeSpeakIcon()
        self.listen = Speak(self.listening, self.changeSpeakIcon)
        self.listen.start()

    def artificialIntelligenceAction(self):
        self.worker = Worker()
        self.worker.start()

    def openBoard(self):
        self.board = Window()
        self.stack.addWidget(self.board)
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def openDictionary(self):
        self.open_dictionary = DictionaryWindow(self.stack)
        self.stack.addWidget(self.open_dictionary)
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)

    def openQuiz(self):
        self.quiz_page = QuizWindow(self.stack)
        self.stack.addWidget(self.quiz_page)
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)