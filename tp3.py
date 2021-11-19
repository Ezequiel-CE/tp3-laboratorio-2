
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import sqlite3



class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("base.ui", self)
        #coneccion a base de datos
        # self.conexion= sqlite3.connect("base3.db")
        # self.cursor= self.conexion.cursor()
        self.nuevo.clicked.connect(self.on_nuevo)
        self.aceptar.clicked.connect(self.on_aceptar)
        self.cancelar.clicked.connect(self.on_cancelar)
        self.lista.itemClicked.connect(self.on_item_clicked)
        self.init_state()
        
    def init_state(self):
        self.form.hide()
        self.form.setEnabled(False)
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        
        
    def on_nuevo(self):
        if self.form.isVisible():
            self.form.hide()
            self.clear_inputs()
        else:
            self.form.show()
            self.form.setEnabled(True)
        
            
    def on_aceptar(self):
        #info para la database
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        correo = self.correo.text()
        telefono = self.telefono.text()
        direccion = self.direccion.text()
        nacimiento = self.nacimiento.text()
        altura = self.altura.text()
        peso = self.peso.text()
        
        self.lista.addItem(f"{nombre} {apellido}")
        self.clear_inputs()
        #habilita los botones
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        
    def on_cancelar(self):
        self.clear_inputs()
        
    def on_item_clicked(self):
        self.confirm_panel.hide()
        print(self.lista.currentItem().text())
        self.nombre.setText(self.lista.currentItem().text())
        self.form.setReadOnly(True)
        
        
    def clear_inputs(self):
        self.nombre.setText("")
        self.apellido.setText("")
        self.correo.setText("")
        self.telefono.setText("")
        self.direccion.setText("")
        self.nacimiento.setText("")
        self.altura.setText("")
        self.peso.setText("")
        
        
        
        
        
        
        
        

app = QApplication([])

win = MiVentana()
win.show()

app.exec_()

