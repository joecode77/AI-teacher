from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize
import sys


class DictionaryDisplay(QMainWindow):
    def __init__(self, stack, text, definition, synonym, antonym):
        super().__init__()
        self.stack = stack
        self.text = text
        self.definition = definition
        self.synonym = synonym
        self.antonym = antonym
        self.createWidgets()
        self.addLayouts()
        self.show()
        
        
    def createWidgets(self):
        self.setStyleSheet("background-color:black; color:white;")

        self.back_button = QPushButton("Back")
        self.back_button.setFont(QFont("Arial", 20))
        self.back_button.setStyleSheet("border:1px solid black;")
        self.back_button.setIcon(QIcon("Dictionary/icons/back.png"))
        self.back_button.clicked.connect(self.goBack)
        self.back_button.setIconSize(QSize(40, 40))

        self.word = QLabel(self.text)
        self.word.setStyleSheet("font-family:Times New Roman;font-size:100px;margin-right:5px;")

        


    def addLayouts(self):
        central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.back_layout = QHBoxLayout()
        self.back_layout.addWidget(self.back_button)
        self.layout.addLayout(self.back_layout)
        self.back_layout.addStretch()
        self.layout.addWidget(QLabel())
       
        self.layout.addWidget(self.word)
        self.layout.addStretch()
        
        if self.definition is not None:
            for part_of_speech in self.definition.keys():
                self.layout.addWidget(QLabel(f"<pre><b><font size = '+2'>       <u>{part_of_speech}<u></font</b></pre>"))
                for specific_meaning in self.definition[part_of_speech]:
                    self.layout.addWidget(QLabel(f"<pre><font size = '+1'>        <ul>{specific_meaning}</font></pre>"))
                self.layout.addStretch()
        else:
            self.layout.addWidget(QLabel(f"<pre><b><font size = '+4'>        {self.text} does not exist in the english dictionary\nor your internet connection is poor</font></b></pre>"))
        self.layout.addStretch()
                    



        
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def goBack(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)
        self.stack.removeWidget(self)

