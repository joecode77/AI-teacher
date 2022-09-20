# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QWidget):
     def __init__(self):
         super().__init__()
         self.tracing_xy = []
         self.lineHistory = []
         self.pen = QPen(Qt.black, 10, Qt.SolidLine)

     def paintEvent(self, QPaintEvent):
         self.painter = QPainter()
         self.painter.begin(self)
         self.painter.setPen(self.pen)

         start_x_temp = 0
         start_y_temp = 0

         if self.lineHistory:
             for line_n in range(len(self.lineHistory)):
                 for point_n in range(1, len(self.lineHistory[line_n])):
                     start_x, start_y = self.lineHistory[line_n][point_n-1][0], self.lineHistory[line_n][point_n-1][1]
                     end_x, end_y = self.lineHistory[line_n][point_n][0], self.lineHistory[line_n][point_n][1]
                     self.painter.drawLine(start_x, start_y, end_x, end_y)

         for x, y in self.tracing_xy:
             if start_x_temp == 0 and start_y_temp == 0:
                 self.painter.drawLine(self.start_xy[0][0], self.start_xy[0][1], x, y)
             else:
                 self.painter.drawLine(start_x_temp, start_y_temp, x, y)

             start_x_temp = x
             start_y_temp = y

         self.painter.end()

     def mousePressEvent(self, QMouseEvent):
         self.start_xy = [(QMouseEvent.pos().x(), QMouseEvent.pos().y())]

     def mouseMoveEvent(self, QMouseEvent):
         self.tracing_xy.append((QMouseEvent.pos().x(), QMouseEvent.pos().y()))
         self.update()

     def mouseReleaseEvent(self, QMouseEvent):
         self.lineHistory.append(self.start_xy+self.tracing_xy)
         self.tracing_xy = []

