from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLineEdit, QLabel, QPushButton, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt

import numpy as np
import sys
import os
import csv

from utils import *

def e():
    sys.exit()

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Rank Everything'
        self.left = 100
        self.top = 100
        self.width = 1600
        self.height = 900
        # self.buttonClicks = 0
        
        self.categories = getCategoryNames()
        self.categoriesCheckBoxes = self.categories.copy()
        print(self.categories)

        self.initUI()

    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # self.grid = QGridLayout()

        ''' Labels '''
        self.label = QLabel(self)
        # self.label.setText("Clicks: " + str(self.buttonClicks))
        # self.label.move(30,0)
       
        ''' Buttons '''
        self.selectCategories = QPushButton('Select Categories', self)
        self.selectCategories.move(100,100)
        self.selectCategories.clicked.connect(self.checkboxChanged)
        
        self.show_text = QPushButton('Show Text', self)
        self.show_text.clicked.connect(self.on_click_show_text)
        self.show_text.move(500,500)

        ''' Textbox '''
        self.textbox = QLineEdit(self)
        self.textbox.setText('Initial text')
        self.textbox.move(500,600)

        ''' Checkbox '''
        self.createCheckboxes()
        
        ''' Layout '''
        # self.grid.addWidget(self.label,     0, 0, alignment=Qt.AlignCenter)
        # self.grid.addWidget(self.check_box, 1, 0, alignment=Qt.AlignCenter)
        # self.grid.addWidget(self.button,    2, 0, alignment=Qt.AlignCenter)
        # self.grid.addWidget(self.show_text, 2, 1, alignment=Qt.AlignCenter)
        # self.grid.addWidget(self.textbox,   3, 0, alignment=Qt.AlignCenter)
        # self.setLayout(self.grid)

        self.show()

    def on_click(self):
        print('button clicked')
        # self.buttonClicks += 1
        self.render_text()
    
    def on_click_show_text(self):
        print('read in text')
        print('Input:', self.textbox.text())

    def on_click_success(self):
        print('showing success alert')
        QMessageBox.information(self, 'Success', 'Update succeeded.', QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")

    def render_text(self):
        # self.label.setText("Clicks: " + str(self.buttonClicks))
        self.update()
    
    def clickBox(self, state):
        if state == Qt.Checked:
            print('Checked')
        else:
            print('Unchecked')

    def checkboxChanged(self):
        print('here')
        for i, v in enumerate(self.categoriesCheckBoxes):
            print(v.text(), "True" if v.checkState() else "False")

    ''' Widgets '''
    def createCheckboxes(self):
        base = 50
        for i, v in enumerate(self.categories):
            self.categoriesCheckBoxes[i] = QCheckBox(v, self)
            self.categoriesCheckBoxes[i].move(500,base)
            base += 25
            print(self.categoriesCheckBoxes)
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = App()
    app.exec_()
    print('Application closed')







