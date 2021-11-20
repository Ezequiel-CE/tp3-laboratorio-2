
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
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
        #evento para los botones de nuevo
        self.aceptar_nuevo.clicked.connect(self.on_aceptar_nuevo)
        self.cancelar_nuevo.clicked.connect(self.on_cancelar)
        #evento para los botones de edit
        self.aceptar_edit.clicked.connect(self.on_aceptar_edit)
        self.cancelar_edit.clicked.connect(self.on_cancelar)
        

        
        self.lista.itemClicked.connect(self.on_item_clicked)
        self.editar.clicked.connect(self.on_editar)
        
        
        self.init_state()
        
    def init_state(self):
        self.form.hide()
        self.confirm_panel_nuevo.hide()
        self.confirm_panel_edit.hide()
        self.form.setEnabled(False)
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        
        
    def on_nuevo(self):
        self.form.show()
        self.form.setEnabled(True)
        self.clear_inputs()
        self.confirm_panel_nuevo.show()
        self.set_readOnlyInputs(False)
        self.confirm_panel_edit.hide()
        
        
        
            
    def on_aceptar_nuevo(self):
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
    
    #funcionalidad para ver items
        
    def on_item_clicked(self):
        self.confirm_panel_nuevo.hide()
        self.nombre.setText(self.lista.currentItem().text())
        #encuentra todos los lineEdits en form
        lineEdits = self.form.findChildren(QLineEdit)
        for lineE in lineEdits:
            lineE.setText(self.lista.currentItem().text())
        self.set_readOnlyInputs(True)
    
    #funcionalidad para editar
    
    def on_editar(self):
        self.set_readOnlyInputs(False)
        self.confirm_panel_edit.show()
        self.nuevo.setEnabled(False)
        self.eliminar.setEnabled(False)
        
    def on_aceptar_edit(self):
        #info para la de los input
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        correo = self.correo.text()
        telefono = self.telefono.text()
        direccion = self.direccion.text()
        nacimiento = self.nacimiento.text()
        altura = self.altura.text()
        peso = self.peso.text()
        
        lineEdits = self.form.findChildren(QLineEdit)
        for lineE in lineEdits:
            lineE.setText("editado")
        
        
        # self.clear_inputs()
        #habilita los botones
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        
        
        
    #funcionalidades auxiliares
    
    
    def clear_inputs(self):
        lineEdits = self.form.findChildren(QLineEdit)
        for line in lineEdits:
            line.setText("")
        
    def set_readOnlyInputs(self,boolean):
        lineEdits = self.form.findChildren(QLineEdit)
        for lineE in lineEdits:
            lineE.setReadOnly(boolean)
        
        
        
        
        
        
        

app = QApplication([])

win = MiVentana()
win.show()

app.exec_()

