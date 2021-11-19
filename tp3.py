
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5 import uic
import sqlite3



class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("base.ui", self)
        #coneccion a base de datos
        self.conexion= sqlite3.connect("base3.db")
        self.cursor= self.conexion.cursor()
        


app = QApplication([])

win = MiVentana()
win.show()

app.exec_()

