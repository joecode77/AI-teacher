from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt
import sys

class QuizWindow(QMainWindow):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.createWidgets()
        self.addLayout()
        self.show()

    def createWidgets(self):
        self.setStyleSheet("background-color: black; color:white;")
        self.back_button = QPushButton("Back")
        self.back_button.setFont(QFont("Arial", 20))
        self.back_button.setStyleSheet("border:1px solid black;")
        self.back_button.setIcon(QIcon("Dictionary/icons/back.png"))
        self.back_button.clicked.connect(self.goBack)
        self.back_button.setIconSize(QSize(40, 40))

        self.title = QLabel("CBT Quizes")
        self.title.setStyleSheet("font-family: monospace; font-size:40px;")
        self.title.setAlignment(Qt.AlignCenter)

        self.waec_card = QPushButton("WAEC")
        self.waec_card.setIcon(QIcon("Quiz/icons/waec.png"))
        self.waec_card.setIconSize(QSize(70, 70))
        self.waec_card.setStyleSheet("padding-top:40px; padding-bottom:40px;font-size:30px; background-color:#6a6a6a;border:1px solid #6a6a6a; border-radius:5px;margin-left:20px; margin-right:20px;")

        self.jamb_card = QPushButton("JAMB")
        self.jamb_card.setIcon(QIcon("Quiz/icons/jamb.png"))
        self.jamb_card.setIconSize(QSize(70, 70))
        self.jamb_card.setStyleSheet("padding-top:40px; padding-bottom:40px;font-size:30px; background-color:#6a6a6a; border:1px solid #6a6a6a;border-radius:5px;margin-left:20px; margin-right:20px;")

    def addLayout(self):
        central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.back_layout = QHBoxLayout()
        self.back_layout.addWidget(self.back_button)
        self.layout.addLayout(self.back_layout)
        self.back_layout.addStretch()
        self.layout.addWidget(QLabel())
       
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.waec_card)
        self.layout.addStretch()
        self.layout.addWidget(self.jamb_card)
        self.layout.addStretch()

        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def goBack(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)
        self.stack.removeWidget(self)




