from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import numpy as np
import sys
import os
import csv

from utils import *
from main_window_frames import *

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
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        formLayout1 = QFormLayout()
        formLayout2 = QFormLayout()
        groupBox1 = QGroupBox("Group Box 1")
        groupBox2 = QGroupBox("Group Box 2")
        
        labelList1 = []
        comboList1 = []
        for i in range(30):
            labelList1.append(QLabel("Label"))
            comboList1.append(QPushButton("Click Me"))
            formLayout1.addRow(labelList1[i], comboList1[i])
        groupBox1.setLayout(formLayout1)
        
        labelList2 = []
        comboList2 = []
        for i in range(30):
            labelList2.append(QLabel("Label"))
            comboList2.append(QPushButton("Click Me"))
            formLayout2.addRow(labelList2[i], comboList2[i])
        groupBox2.setLayout(formLayout2)
        
        scroll1 = QScrollArea()
        scroll1.setWidget(groupBox1)
        scroll1.setWidgetResizable(True)
        scroll1.setFixedHeight(900)
        scroll1.setFixedWidth(500)

        scroll2 = QScrollArea()
        scroll2.setWidget(groupBox2)
        scroll2.setWidgetResizable(True)
        scroll2.setFixedHeight(900)
        scroll2.setFixedWidth(500)
        
        
        layout = QHBoxLayout(self)
        layout.addWidget(scroll1)
        layout.addWidget(scroll2)
        self.show()





        # ''' Labels '''
        # self.currentLists = QLabel('Current Lists', self)
        # self.currentLists.move(25,25)
       
        # ''' Buttons '''
        # self.selectCategories = QPushButton('Select Categories', self)
        # self.selectCategories.move(25,50)
        # self.selectCategories.clicked.connect(self.checkboxChanged)
        
        # self.show_text = QPushButton('Show Text', self)
        # self.show_text.clicked.connect(self.on_click_show_text)
        # self.show_text.move(500,500)

        # ''' Textbox '''
        # self.textbox = QLineEdit(self)
        # self.textbox.setText('Initial text')
        # self.textbox.move(500,600)

        # ''' Checkbox '''
        # self.createCheckboxes()
        
        # ''' Scroll Area '''
        # self.scroll_area = QScrollArea()
        # self.scroll_area.setFixedWidth(250)
        # self.scroll_area.setWidgetResizable(True)
        
        # widget = QWidget()
        # self.scroll_area.setWidget(widget)
        # self.layout_scroll_area = QVBoxLayout(widget)
        # self.layout_scroll_area.addWidget(self.show_text)
        
        # ''' Layout '''
        # # self.grid.addWidget(self.check_box, 1, 0, alignment=Qt.AlignCenter)
        # # self.grid.addWidget(self.button,    2, 0, alignment=Qt.AlignCenter)
        # # self.grid.addWidget(self.show_text, 2, 1, alignment=Qt.AlignCenter)
        # # self.grid.addWidget(self.textbox,   3, 0, alignment=Qt.AlignCenter)
        # # self.grid.addWidget(self.scroll_area, 4, 0, alignment=Qt.AlignCenter)
        # # self.setLayout(self.grid)
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.scroll_area)
        # self.setLayout(self.layout)
        
        # self.show()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = App()
    app.exec_()
    print('Application closed')







