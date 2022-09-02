from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import QThread
from classroom import ClassRoom
import sounddevice as sd
import soundfile as sf
import sys


class WelcomeScreen(QMainWindow):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.createWidgets()
        self.createLayouts()
        self.setWindowTitle("Socrates")
        self.setStyleSheet("background-color:#000000;")
        self.show()
        
        
    def createWidgets(self):
        self.title = QLabel("Socrates")
        self.title.setFont(QFont("Arial", 15))
        self.title.setStyleSheet("color:#dedede; margin-left:90px;")

        self.heading_top = QLabel("Virtual")
        self.heading_top.setFont(QFont("tahoma", 70))
        self.heading_top.setStyleSheet("color: #3e68dc; text-decoration:underline; margin-left:90px;")

        self.heading_buttom = QLabel("teacher") 
        self.heading_buttom.setFont(QFont("Ariel", 70))
        self.heading_buttom.setStyleSheet("color:#ffffff; margin-left:90px;")

        self.slogan = QLabel("A teacher for every student")
        self.slogan.setFont(QFont("Ariel", 20))
        self.slogan.setStyleSheet("color:#838383; margin-left:90px;")

        self.next_button = QPushButton("Let's Discuss")
        self.next_button.setFont(QFont("Ariel", 17))
        self.next_button.clicked.connect(self.moveToNextPage)
        self.next_button.setStyleSheet("background-color:#4270f6; color:white; border-radius:50px; margin-left:90px;")
        
        self.movie = QMovie("gifs/_ (1).gif")
        self.scifi_gif = QLabel()
        self.scifi_gif.setMovie(self.movie)
        self.movie.start()

        self.AUDIO_PATH = "audio/welcome.wav"
        data, fs = sf.read(self.AUDIO_PATH, dtype = 'float32')
        sd.play(data, fs)

        
        

    def createLayouts(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QHBoxLayout()
        first_half_layout = QVBoxLayout()
        second_half_layout = QVBoxLayout()

        first_half_layout.addWidget(self.title)
        first_half_layout.addStretch(3)
        first_half_layout.addWidget(self.heading_top)
        first_half_layout.addWidget(self.heading_buttom)
        first_half_layout.addWidget(self.slogan)
        first_half_layout.addStretch(1)
        first_half_layout.addWidget(self.next_button)
        first_half_layout.addStretch(3)

        second_half_layout.addWidget(self.scifi_gif)

        self.central_widget.setLayout(layout)
        layout.addLayout(first_half_layout)
        layout.addLayout(second_half_layout)


    def moveToNextPage(self):
        sd.stop()
        class_ = ClassRoom(self.stack)
        self.stack.addWidget(class_)
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)
    