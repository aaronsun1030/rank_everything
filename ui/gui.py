from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
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
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layoutCategorySection = QVBoxLayout()
        layoutItem1Section = QVBoxLayout()
        layoutItem2Section = QVBoxLayout()
        groupBoxCategory = QGroupBox("Categories")
        groupBoxItem1 = QGroupBox("Item 1")
        groupBoxItem2 = QGroupBox("Item 2")
        
        #=====================================================================#
        # Left side scroll bar widgets/layouts
        #=====================================================================#

        ''' labels for selected categories '''
        # create labels and initial NONE label
        labelSelectedCategories = QLabel('Selected Categories', self)
        labelSelectedCategories.setFont(QFont("Times",weight=QFont.Bold))
        labelSelectedCategories.setFixedHeight(30)
        labelNONE = QLabel('NONE', self)
        labelNONE.setFixedHeight(30)

        # create layout and add widgets to overall layout
        self.layoutCategoriesSelected = QVBoxLayout()
        self.layoutCategoriesSelected.addWidget(labelSelectedCategories)
        self.layoutCategoriesSelected.addWidget(labelNONE)
        layoutCategorySection.addLayout(self.layoutCategoriesSelected)

        ''' buttons in categories '''
        # define button and events
        buttonUpdateCategories = QPushButton('Update List', self)
        buttonUpdateCategories.clicked.connect(self.checkboxChanged)
        buttonBeginRating = QPushButton('Begin Rating', self)
        buttonBeginRating.clicked.connect(self.beginRating)

        # create layout and add widgets to overall layout
        self.layoutCategoryButtons = QHBoxLayout()
        self.layoutCategoryButtons.addWidget(buttonUpdateCategories)
        self.layoutCategoryButtons.addWidget(buttonBeginRating)
        layoutCategorySection.addLayout(self.layoutCategoryButtons)

        ''' category checkboxes '''
        # get categories and create checkboxes
        self.checkedCategories = [] # contains the current selected categories
        self.categories = sorted(getCategoryNames())
        for i in range(100):
            self.categories.append(str(i+1))
        self.layoutCategoryCheckboxes = QVBoxLayout()
        self.checkboxCategories = self.categories.copy()
        for i, v in enumerate(self.categories):
            self.checkboxCategories[i] = QCheckBox(v, self)
            self.layoutCategoryCheckboxes.addWidget(self.checkboxCategories[i])

        # add to layout
        layoutCategorySection.addLayout(self.layoutCategoryCheckboxes)
        groupBoxCategory.setLayout(layoutCategorySection)
        
        #=====================================================================#
        # Middle scroll bar for item 1
        #=====================================================================#
        
        self.layoutItem1 = QVBoxLayout()
        layoutItem1Section.addLayout(self.layoutItem1)
        groupBoxItem1.setLayout(layoutItem1Section)
        
        #=====================================================================#
        # Right scroll bar for item 2
        #=====================================================================#

        labelList3 = []
        for i in range(100):
            labelList3.append(QLabel("Label" + str(i)))
            layoutItem2Section.addWidget(labelList3[i])
        groupBoxItem2.setLayout(layoutItem2Section)
        
        #=====================================================================#
        # Define scroll area and create final layout
        #=====================================================================#

        scrollCategory = QScrollArea()
        scrollCategory.setWidget(groupBoxCategory)
        scrollCategory.setWidgetResizable(True)
        scrollCategory.setFixedHeight(900)
        scrollCategory.setFixedWidth(300)

        scrollItem1 = QScrollArea()
        scrollItem1.setWidget(groupBoxItem1)
        scrollItem1.setWidgetResizable(True)
        scrollItem1.setFixedHeight(900)
        scrollItem1.setFixedWidth(600)

        scrollItem2 = QScrollArea()
        scrollItem2.setWidget(groupBoxItem2)
        scrollItem2.setWidgetResizable(True)
        scrollItem2.setFixedHeight(900)
        scrollItem2.setFixedWidth(600)

        layout = QHBoxLayout(self)
        layout.addWidget(scrollCategory)
        layout.addWidget(scrollItem1)
        layout.addWidget(scrollItem2)
        
        self.show()

        # ''' Textbox '''
        # self.textbox = QLineEdit(self)
        # self.textbox.setText('Initial text')
        # self.textbox.move(500,600)

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
        print('detected change in checkboxes:')
        # delete layout widgets and add base header
        self.clearLayout(self.layoutCategoriesSelected)
        labelSelectedCategories = QLabel('Selected Categories', self)
        labelSelectedCategories.setFont(QFont("Times",weight=QFont.Bold))
        labelSelectedCategories.setFixedHeight(30)
        self.layoutCategoriesSelected.addWidget(labelSelectedCategories)
        
        # get checked categories
        self.checkedCategories = []
        for i, v in enumerate(self.checkboxCategories):
            if v.checkState():
                self.checkedCategories.append(v.text())
        
        # add
        if self.checkedCategories == []:
            print('nothing checked')
            labelNONE = QLabel('NONE', self)
            labelNONE.setFixedHeight(30)
            self.layoutCategoriesSelected.addWidget(labelNONE)
        else:
            print(self.checkedCategories)
            for name in self.checkedCategories: 
                _labelName = QLabel(name, self)
                _labelName.setFixedHeight(20)
                self.layoutCategoriesSelected.addWidget(_labelName)

    def beginRating(self):
        print('begin rating with selected categories:')
        if self.checkedCategories == []:
            print('no categories selected')
            return
        print(self.checkedCategories)
        # self.renderItemLayout(item1, self.layoutItem1)
        # self.renderItemLayout(item2, self.layoutItem2)


        


    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = App()
    app.exec_()
    print('Application closed')



