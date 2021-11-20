
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5 import uic
import sqlite3



class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("base.ui", self)
        #coneccion a base de datos
        self.conexion= sqlite3.connect("base3.db")
        self.cursor= self.conexion.cursor()
        self.nuevo.clicked.connect(self.on_nuevo)
        #registro de usuarios
        self.usersArr = []
        #orden ususarios
        self.order = 0
        self.lastID = 0
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
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.carga()
        
        
    def carga(self):
        self.cursor.execute("select * from usuarios")
        usuarios = self.cursor.fetchall()
        #guarda cada usuario en un diccionario y lo empuja a un array
        for idN,nombre,apellido,mail,telefono,direccion,nacimiento,altura,peso in usuarios:
            user={"order": self.order,"id":idN,"nombre":nombre,"apellido":apellido,"mail":mail,"telefono":telefono,"direccion":direccion,"nacimiento":nacimiento,"altura":altura,"peso":peso}
            self.usersArr.append(user)
            self.lista.addItem(f"{nombre} {apellido}")
            #aumenta el orden
            self.order += 1
            self.lastID = idN
            print(user)
        
        
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
        mail = self.correo.text()
        telefono = self.telefono.text()
        direccion = self.direccion.text()
        nacimiento = self.nacimiento.text()
        altura = self.altura.text()
        peso = self.peso.text()
        
        self.cursor.execute(f"INSERT INTO usuarios(nombre,apellido,mail,telefono,direccion,nacimiento,altura,peso) VALUES ('{nombre}','{apellido}','{mail}','{telefono}','{direccion}','{nacimiento}','{altura}','{peso}')")
        self.conexion.commit()
        self.lista.addItem(f"{nombre} {apellido}")
        user={"order": self.order,"id":self.lastID+1,"nombre":nombre,"apellido":apellido,"mail":mail,"telefono":telefono,"direccion":direccion,"nacimiento":nacimiento,"altura":altura,"peso":peso}
        self.usersArr.append(user)
        print(user)
        self.clear_inputs()
        #habilita los botones
        self.confirm_panel_nuevo.hide()
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        
    def on_cancelar(self):
        self.clear_inputs()
    
    #funcionalidad para ver items
        
    def on_item_clicked(self):
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.editar.setEnabled(True)
        
        self.form.show()
        self.confirm_panel_nuevo.hide()
        current_index= self.lista.currentRow()
        current_user = self.usersArr[current_index]
        self.fill_user(current_user)
        self.set_readOnlyInputs(True)
        
    def fill_user(self,diccionario):
        self.nombre.setText(diccionario["nombre"])
        self.apellido.setText(diccionario["apellido"])
        self.correo.setText(diccionario["mail"])
        self.telefono.setText(diccionario["telefono"])
        self.direccion.setText(diccionario["direccion"])
        self.nacimiento.setText(diccionario["nacimiento"])
        self.altura.setText(str(diccionario["altura"]))
        self.peso.setText(str(diccionario["peso"]))
        
    
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

