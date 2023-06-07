################ Import pip ############################
import pip
#########################################################

################# Install packages if not already installed ###########
#######################################################################
def import_or_install(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])

import_or_install("varname")
import_or_install("csv")
import_or_install("math")
import_or_install("sys")
import_or_install("PyQt5")


################# Import libraries #######################
##########################################################
from varname import nameof
import csv
import math

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt



class Grid(QWidget):
    def __init__(self, rows, columns):
        super().__init__()
        self.clicked_cells = []
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.clicked_color = QColor(Qt.green)
        self.default_color = QColor(Qt.white)
        self.buttons = []
        self.setFixedSize(1750,950)


        for row in range(-1, rows):
            for col in range(-1, columns):
                if row == -1 and col == -1:
                    button = QPushButton("All")
                    button.clicked.connect(lambda: self.all_clicked(columns, rows))
                #else:
                    #button = QPushButton(f"{chr(row + ord('A')) if row != -1 else ''}{col + 1 if col != -1 else ''}")
                    #self.buttons.append(button)
                else:
                    quotient, remainder = divmod(row, 26)
                    first_letter = chr(quotient + ord('A') - 1) if quotient > 0 else ''
                    second_letter = chr(remainder + ord('A'))
                    button = QPushButton(f"{first_letter if row != -1 else ''}{second_letter if row != -1 else ''}{col + 1 if col != -1 else ''}")
                    self.buttons.append(button)
                if row != -1 and col != -1:
                    button.clicked.connect(lambda _, button=button: self.cell_clicked(button))
                elif row == -1:
                    button.clicked.connect(lambda _, col=col: self.column_clicked(col, rows))
                elif col == -1:
                    button.clicked.connect(lambda _, row=row: self.row_clicked(row, columns))
                button.setAutoFillBackground(True)
                self.grid.addWidget(button, row + 1, col + 1)
        self.setLayout(self.grid)
        self.show()

    def all_clicked(self, columns, rows):
        for row in range(0, rows):
            for col in range(-1, columns):
                button = self.grid.itemAtPosition(row + 1, col + 1).widget()
                if button.text() not in self.clicked_cells:
                    self.clicked_cells.append(button.text())
                    button.setStyleSheet(f'background-color: {self.clicked_color.name()}')
                else:
                    self.clicked_cells.remove(button.text())
                    button.setStyleSheet(f'background-color: {self.default_color.name()}')

    def column_clicked(self, col, rows):
        for row in range(rows):
            button = self.grid.itemAtPosition(row + 1, col + 1).widget()
            if button.text() not in self.clicked_cells:
                self.clicked_cells.append(button.text())
                button.setStyleSheet(f'background-color: {self.clicked_color.name()}')
            else:
                self.clicked_cells.remove(button.text())
                button.setStyleSheet(f'background-color: {self.default_color.name()}')

    def row_clicked(self, row, columns):
        for col in range(columns):
            button = self.grid.itemAtPosition(row + 1, col + 1).widget()
            if button.text() not in self.clicked_cells:
                self.clicked_cells.append(button.text())
                button.setStyleSheet(f'background-color: {self.clicked_color.name()}')
            else:
                self.clicked_cells.remove(button.text())
                button.setStyleSheet(f'background-color: {self.default_color.name()}')

    def cell_clicked(self, button):
        if button.text() in self.clicked_cells:
            self.clicked_cells.remove(button.text())
            button.setStyleSheet(f'background-color: {self.default_color.name()}')
        else:
            self.clicked_cells.append((button.text()))
            button.setStyleSheet(f'background-color: {self.clicked_color.name()}')

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.close()

def generate_grid(rows, columns):
    app = QApplication([])
    grid = Grid(rows, columns)
    app.exec_()
    return grid.clicked_cells

#clicked_cells = generate_grid(32, 48)
#print(clicked_cells)
