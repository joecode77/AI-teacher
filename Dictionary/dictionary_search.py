from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize
from PyDictionary import PyDictionary
from Dictionary.dictionary_display import DictionaryDisplay
import threading
import sys


class DictionaryWindow(QMainWindow):
    def __init__(self, stack):
        super().__init__()
        # self.initializeUI()
        self.createWidgets()
        self.addLayouts()
        self.dictionary = PyDictionary()
        self.stack = stack
        self.definition = False
        self.synonym_result = False
        self.antonym_result = False
        self.show()

    # def initializeUI(self):
        # self.resize(500, 500)
        # self.setWindowTitle("Dictionary")

    def createWidgets(self):
        self.setStyleSheet("background-color:black; color:white;")

        self.back_button = QPushButton("Back")
        self.back_button.setFont(QFont("Arial", 20))
        self.back_button.setStyleSheet("border:1px solid black;")
        self.back_button.setIcon(QIcon("Dictionary/icons/back.png"))
        self.back_button.clicked.connect(self.goBack)
        self.back_button.setIconSize(QSize(40, 40))

        self.label = QLabel("<b>Dictionary<b>")

        # self.label.setFont(QFont("Helvetica", 30))
        self.label.setStyleSheet(
            "font-family:Times New Roman; font-size:90px; margin-left:30px;")

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search")
        self.search.setFont(QFont("Arial", 20))
        self.search.setStyleSheet("margin-left:50px; padding:5px;")

        self.search_button = QPushButton()
        self.search_button.setStyleSheet(
            "padding:20px; border:1px solid black; margin-right:5px;")
        self.search_button.setIcon(QIcon("Dictionary/icons/search.png"))
        self.search_button.setIconSize(QSize(50, 50))
        self.search_button.clicked.connect(self.getDefinition)
        # self.search.addIcon(QIcon("voice_listening.png"))

    def addLayouts(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()
        self.back_layout = QHBoxLayout()
        self.back_layout.addWidget(self.back_button)
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search)
        self.search_layout.addWidget(self.search_button)

        self.layout.addLayout(self.back_layout)
        self.back_layout.addStretch()
        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.search_layout)
        self.layout.addStretch(2)
        central_widget.setLayout(self.layout)

    def getDefinition(self):
        text = self.search.text()
        print(text)

        def define():
            self.definition = self.dictionary.meaning(text)
            print("DEFINITION", self.definition)


        def synonym():
            self.synonym_result = self.dictionary.synonym(text)

        def antonym():
            self.antonym_result = self.dictionary.antonym(text)

        t1 = threading.Thread(target=define)
        t2 = threading.Thread(target=synonym)
        t3 = threading.Thread(target=antonym)

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

        display = DictionaryDisplay(self.stack, text, self.definition, self.synonym_result, self.antonym_result)
        self.stack.addWidget(display)
        self.stack.setCurrentIndex(self.stack.currentIndex() + 1)


    def goBack(self):
        self.stack.setCurrentIndex(self.stack.currentIndex() - 1)
        self.stack.removeWidget(self)


    # def changeFont(self):
    #     self.layout.removeWidget(self.button)
