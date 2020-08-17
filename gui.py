from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import numpy as np
import sys
import os
import csv

from utils import *
from compare_objects import *

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

        self._item_name_1 = None
        self._item_name_2 = None
        self._item_description_1 = None
        self._item_description_2 = None
        self._item_tags_1 = None
        self._item_tags_2 = None
        self._item_thoughts_1 = None
        self._item_thoughts_2 = None
        self.item1, self.item2 = None, None

        self.comparator = Comparator()
        
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
        labelSelectedCategories = self.createLabelBold('Selected Categories')
        labelNONE = self.createLabel('(NONE)')
        
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

        self.layoutItem2 = QVBoxLayout()
        layoutItem2Section.addLayout(self.layoutItem2)
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

    def on_click_success(self):
        print('showing success alert')
        QMessageBox.information(self, 'Success', 'Update succeeded.', QMessageBox.Ok, QMessageBox.Ok)

    def checkboxChanged(self):
        print('detected change in checkboxes:')
        # delete layout widgets and add base header
        self.clearLayout(self.layoutCategoriesSelected)
        labelSelectedCategories = self.createLabelBold('Selected Categories')
        self.layoutCategoriesSelected.addWidget(labelSelectedCategories)
        
        # get checked categories
        self.checkedCategories = []
        for i, v in enumerate(self.checkboxCategories):
            if v.checkState():
                self.checkedCategories.append(v.text())
        
        # add checked categories to list
        if self.checkedCategories == []:
            print('nothing checked')
            labelNONE = self.createLabel('(NONE)')
            self.layoutCategoriesSelected.addWidget(labelNONE)
        else:
            print(self.checkedCategories)
            for name in self.checkedCategories: 
                _labelName = self.createLabel(name)
                self.layoutCategoriesSelected.addWidget(_labelName)

    def beginRating(self):
        print('begin rating with selected categories:')
        if self.checkedCategories == []:
            print('no categories selected')
            return
        print(self.checkedCategories)

        # add list
        for name in self.checkedCategories:
            self.comparator.add_list(name)
        print('lists in comparator:', self.comparator.get_active_lists())

        # shuffle
        print('shuffling items')
        self.comparator.shuffle_pair()
        self.item1, self.item2 = self.comparator.get_pair()
        self.renderItemLayout1(self.item1, self.layoutItem1)
        self.renderItemLayout2(self.item2, self.layoutItem2)

    def renderItemLayout1(self, item, layout):
        # item id
        labelItemId = self.createLabelBold('ID')
        label_item_id = self.createLabel(item.get_item_id())

        layout.addWidget(labelItemId)
        layout.addWidget(label_item_id)

        # item name
        labelItemName = self.createLabelBold('Name')
        self._item_name_1 = self.createQTextEdit(item.get_name())
        b = QPushButton('Edit', self)
        b.clicked.connect(self.editName_1)
        
        layout.addWidget(labelItemName)
        layout.addWidget(self._item_name_1)
        layout.addWidget(b)

        # item description
        labelItemDescription = self.createLabelBold('Description')
        self._item_description_1 = self.createQTextEdit(item.get_description())
        
        layout.addWidget(labelItemDescription)
        layout.addWidget(self._item_description_1)

        # item tags
        labelItemTags = self.createLabelBold('Tags')
        self._item_tags_1 = self.createQTextEdit(str(item.get_tags()))
        
        layout.addWidget(labelItemTags)
        layout.addWidget(self._item_tags_1)

        # item thoughts
        labelItemThoughts = self.createLabelBold('Thoughts')
        self._item_thoughts_1 = self.createQTextEdit(item.get_thoughts())
        
        layout.addWidget(labelItemThoughts)
        layout.addWidget(self._item_thoughts_1)

        # prefer button
        buttonPreferItem1 = QPushButton('Prefer Item 1', self)
        buttonPreferItem1.clicked.connect(self.onClickPreferItem1)
        
        layout.addWidget(buttonPreferItem1)

    def renderItemLayout2(self, item, layout):
        # item id
        labelItemId = self.createLabelBold('ID')
        label_item_id = self.createLabel(item.get_item_id())

        layout.addWidget(labelItemId)
        layout.addWidget(label_item_id)

        # item name
        labelItemName = self.createLabelBold('Name')
        self._item_name_2 = self.createQTextEdit(item.get_name())
        
        layout.addWidget(labelItemName)
        layout.addWidget(self._item_name_2)

        # item description
        labelItemDescription = self.createLabelBold('Description')
        self._item_description_2 = self.createQTextEdit(item.get_description())
        
        layout.addWidget(labelItemDescription)
        layout.addWidget(self._item_description_2)

        # item tags
        labelItemTags = self.createLabelBold('Tags')
        self._item_tags_2 = self.createQTextEdit(str(item.get_tags()))
        
        layout.addWidget(labelItemTags)
        layout.addWidget(self._item_tags_2)

        # item thoughts
        labelItemThoughts = self.createLabelBold('Thoughts')
        self._item_thoughts_2 = self.createQTextEdit(item.get_thoughts())
        
        layout.addWidget(labelItemThoughts)
        layout.addWidget(self._item_thoughts_2)

        # prefer button
        buttonPreferItem2 = QPushButton('Prefer Item 2', self)
        buttonPreferItem2.clicked.connect(self.onClickPreferItem2)

        layout.addWidget(buttonPreferItem2)
        
    def onClickPreferItem1(self):
        self.comparator.select_preferred(1)
        self.comparator.shuffle_pair()
        self.clearLayout(self.layoutItem1)
        self.clearLayout(self.layoutItem2)

    def onClickPreferItem2(self):
        self.comparator.select_preferred(2)
        self.comparator.shuffle_pair()
        self.clearLayout(self.layoutItem1)
        self.clearLayout(self.layoutItem2)

    def createLabelBold(self, name):
        label = QLabel(name, self)
        label.setFont(QFont("Times",weight=QFont.Bold))
        label.setFixedHeight(30)
        return label

    def createLabel(self, name):
        label = QLabel(name, self)
        label.setFixedHeight(20)
        return label

    def createQTextEdit(self, text):
        textbox = QTextEdit(self)
        textbox.setText(text)
        return textbox

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    ''' button handlers for editing text in csv '''
    def editName_1(self):
        print('edit')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = App()
    app.exec_()
    print('Application closed')


