from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QCheckBox
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
        
        ''' Labels '''
        self.label = QLabel(self)
        self.label.setText("Clicks: " + str(self.buttonClicks))
        # self.label.move(30,0)
       
        ''' Buttons '''
        self.button = QPushButton('Click', self)
        # self.button.setText('Y')
        # self.button.move(0,100)
        self.button.clicked.connect(self.on_click)
        self.button.setShortcut("Y")
        
        self.show_text = QPushButton('Show Text', self)
        self.show_text.clicked.connect(self.on_click_show_text)

        ''' Textbox '''
        self.textbox = QLineEdit(self)
        self.textbox.setText('Initial text')
        
        ''' Checkbox '''
        self.check_box = QCheckBox("Test Box", self)
        self.check_box.stateChanged.connect(self.clickBox)

        ''' Layout '''
        self.grid = QGridLayout()
        self.grid.addWidget(self.label,     0, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.check_box, 1, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.button,    2, 0, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.show_text, 2, 1, alignment=Qt.AlignCenter)
        self.grid.addWidget(self.textbox,   3, 0, alignment=Qt.AlignCenter)
        self.setLayout(self.grid)

        self.show()

    def on_click(self):
        print('button clicked')
        self.buttonClicks += 1
        self.render_text()
    
    def on_click_show_text(self):
        print('read in text')
        print('Input:', self.textbox.text())

    def on_click_success(self):
        print('showing success alert')
        QMessageBox.information(self, 'Success', 'Update succeeded.', QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    def render_text(self):
        self.label.setText("Clicks: " + str(self.buttonClicks))
        self.update()
    
    def clickBox(self, state):
        if state == Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = App()
    app.exec_()
    print('Application closed')







