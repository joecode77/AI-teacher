from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget
from welcome_screen import WelcomeScreen
from classroom import ClassRoom
import sys

# style_sheet = """
#     # QWidget{
#     #     background-color: black;
#     # }

#     QLabel#welcome_heading_top{
#         color:#426ff7;
#     }

#     QLabel#welcome_heading_bottom{
#         color:#fdfdfd;
#     )

# """
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(styles
    widget = QStackedWidget()
    welcome = WelcomeScreen(widget)
    # welcome.setStyleSheet(style_sheet)

    widget.addWidget(welcome)
    widget.setWindowTitle("Socrates")
    widget.resize(700, 700)

    widget.show()

    sys.exit(app.exec_())