from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

import numpy as np
from matplotlib import pyplot as plt
import sys
import os
import csv



def e():
    sys.exit()



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Rank Everything'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 1000
        self.buttonClicks = 0
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Clicks: " + str(self.buttonClicks))
        # self.label.move(30,0)
       
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Y')
        # self.b1.move(0,100)
        self.b1.clicked.connect(self.on_click_b1)
        self.b1.setShortcut("Y")
        
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText('N')
        # self.b2.move(100,100)
        self.b2.clicked.connect(self.on_click_b2)
        self.b2.setShortcut("N")

        
        self.grid = QGridLayout()
        self.grid.addWidget(self.label,      0, 1, alignment=Qt.AlignTop|Qt.AlignCenter)
        self.grid.addWidget(self.b1,         0, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.b2,         0, 2, alignment=Qt.AlignCenter)
        self.setLayout(self.grid)

        self.show()

    def on_click_b1(self):
        print('b1 clicked')
        self.buttonClicks += 1
        self.render_text()
    
    def on_click_b2(self):
        print('b2 clicked')
        self.buttonClicks += 1
        self.render_text()
    
    def render_text(self):
        self.label.setText("Clicks: " + str(self.buttonClicks))
        self.update()
    
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = App()
    app.exec_()
    print('Application closed.')







