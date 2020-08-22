from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

import numpy as np
import sys
import os
import csv

def e():
    sys.exit()

class WindowUpdateThoughts(QWidget):

    def __init__(self, mainWindow):
        super().__init__()
        self.title = 'Update Thoughts'
        self.left = 100
        self.top = 100
        self.width = 1600
        self.height = 900
        
        self.mainWindow = mainWindow
        self.currentItem = None
        self.textEditNewThoughts = None

        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Left pane
        self.layoutLeftSection = QVBoxLayout()
        groupBoxLeftPane = QGroupBox("Past Thoughts")
        groupBoxLeftPane.setLayout(self.layoutLeftSection)
        
        # Right pane
        self.layoutRightSection = QVBoxLayout()
        groupBoxRightPane = QGroupBox("New Thoughts")
        groupBoxRightPane.setLayout(self.layoutRightSection)

        # Scroll areas
        scrollLeftPane = QScrollArea()
        scrollLeftPane.setWidget(groupBoxLeftPane)
        scrollLeftPane.setWidgetResizable(True)
        scrollLeftPane.setFixedHeight(800)
        scrollLeftPane.setFixedWidth(700)

        scrollRightPane = QScrollArea()
        scrollRightPane.setWidget(groupBoxRightPane)
        scrollRightPane.setWidgetResizable(True)
        scrollRightPane.setFixedHeight(800)
        scrollRightPane.setFixedWidth(700)

        #=====================================================================#
        # Final layout
        #=====================================================================# 

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(scrollLeftPane)
        self.layout.addWidget(scrollRightPane)

    def onClickUpdateThoughts(self):
        print('updating thoughts')
        QMessageBox.information(self, 'Success', 'Update succeeded.', QMessageBox.Ok, QMessageBox.Ok)
        self.hide()
        self.clearFrames()
        self.currentItem.add_thought(self.textEditNewThoughts.toPlainText())
        
        self.mainWindow.renderItemLayout1(self.mainWindow.item1, self.mainWindow.layoutItem1)
        self.mainWindow.renderItemLayout2(self.mainWindow.item2, self.mainWindow.layoutItem2)
        
        self.mainWindow.show()
        print('going back to main window')

    def onClickCancel(self):
        print('cancelling update')
        QMessageBox.information(self, 'Success', 'No update made.', QMessageBox.Ok, QMessageBox.Ok)
        self.hide()
        self.clearFrames()
        self.mainWindow.show()
        print('going back to main window')
    
    def on_click_success(self):
        print('showing success alert')
        QMessageBox.information(self, 'Success', 'Update succeeded.', QMessageBox.Ok, QMessageBox.Ok)

    def renderWindow(self, num):
        self.currentItem = self.mainWindow.item1 if num == 1 else self.mainWindow.item2
        self.renderLeftPane()
        self.renderRightPane()

    def renderLeftPane(self):
        thoughtsString = self.currentItem.get_thoughts()
        textEditPastThoughts = self.createQTextEdit(thoughtsString)
        textEditPastThoughts.setReadOnly(True)

        self.layoutLeftSection.addWidget(textEditPastThoughts)
        
    def renderRightPane(self):
        componentVLayout = QVBoxLayout()

        self.textEditNewThoughts = self.createQTextEdit('Add Thoughts Here.')
        self.textEditNewThoughts.setFixedHeight(700)

        # horizontal layout for buttons
        layoutButtons = QHBoxLayout()
        
        buttonUpdate = QPushButton("Update")
        buttonUpdate.clicked.connect(self.onClickUpdateThoughts)

        buttonCancel = QPushButton("Cancel")
        buttonCancel.clicked.connect(self.onClickCancel)
        
        layoutButtons.addWidget(buttonUpdate)
        layoutButtons.addWidget(buttonCancel)
        
        # add sublayouts to main layout
        componentVLayout.addWidget(self.textEditNewThoughts)
        componentVLayout.addLayout(layoutButtons)

        # add to main frame
        frameRight = QFrame()
        frameRight.setLayout(componentVLayout)

        self.layoutRightSection.addWidget(frameRight)
        
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

    def clearFrames(self):
        self.clearLayout(self.layoutLeftSection)
        self.clearLayout(self.layoutRightSection)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
