
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit,QMessageBox
from PyQt5 import uic
import sqlite3



class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("base.ui", self)
        #coneccion a base de datos
        self.conexion= sqlite3.connect("base3.db")
        self.cursor= self.conexion.cursor()
        #registro de usuarios
        self.usersArr = []
        #usuario actual
        self.currentUser = ""
        #evento para los botones de nuevo
        self.aceptar_nuevo.clicked.connect(self.on_aceptar_nuevo)
        self.cancelar_nuevo.clicked.connect(self.on_cancelar_nuevo)
        #evento para los botones de edit
        self.aceptar_edit.clicked.connect(self.on_aceptar_edit)
        self.cancelar_edit.clicked.connect(self.on_cancelar_edit)
        #botones de funcionalidades
        self.nuevo.clicked.connect(self.on_nuevo)
        self.lista.itemClicked.connect(self.on_item_clicked)
        self.editar.clicked.connect(self.on_editar)
        self.eliminar.clicked.connect(self.on_eliminar)
        
        
        
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
        #no hace nada si esta vacio la base de datos
        if(len(usuarios) < 1): return
        #guarda cada usuario en un diccionario y lo empuja a un array
        for idN,nombre,apellido,mail,telefono,direccion,nacimiento,altura,peso in usuarios:
            user={"id":idN,"nombre":nombre,"apellido":apellido,"mail":mail,"telefono":telefono,"direccion":direccion,"nacimiento":nacimiento,"altura":altura,"peso":peso}
            self.usersArr.append(user)
            self.lista.addItem(f"{nombre} {apellido}")
            
            
    #funcionalidad para nuevo
        
    def on_nuevo(self):
        self.form.show()
        self.form.setEnabled(True)
        self.clear_inputs()
        self.confirm_panel_nuevo.show()
        self.set_readOnlyInputs(False)
        self.confirm_panel_edit.hide()
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        
        
        
        
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
        user={"id":self.cursor.lastrowid,"nombre":nombre,"apellido":apellido,"mail":mail,"telefono":telefono,"direccion":direccion,"nacimiento":nacimiento,"altura":altura,"peso":peso}
        #self.cursor.lastrowid debuelve el ultimo id insertado
        self.usersArr.append(user)
        print(user)
        self.clear_inputs()
        #habilita los botones
        self.confirm_panel_nuevo.hide()
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        #pone focus en el recien agregado
        self.lista.item(self.lista.count()-1).setSelected(True)
        self.fill_user(user)
        self.set_readOnlyInputs(True)
        
    def on_cancelar_nuevo(self):
        self.clear_inputs()
        self.set_readOnlyInputs(True)
        self.form.hide()
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
    
    #funcionalidad para ver items
        
    def on_item_clicked(self):
        #habilita los botones
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.editar.setEnabled(True)
        
        self.form.show()
        self.confirm_panel_nuevo.hide()
        current_index= self.lista.currentRow()
        self.current_user = self.usersArr[current_index]
        self.fill_user(self.current_user)
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
        self.confirm_panel_nuevo.hide()
        self.nuevo.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.editar.setEnabled(False)
        
        
    def on_aceptar_edit(self):
        #info para la de los input
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        mail = self.correo.text()
        telefono = self.telefono.text()
        direccion = self.direccion.text()
        nacimiento = self.nacimiento.text()
        altura = self.altura.text()
        peso = self.peso.text()
        #encuenta el ususario en array y lo edita
        user_editado={"id":self.current_user["id"],"nombre":nombre,"apellido":apellido,"mail":mail,"telefono":telefono,"direccion":direccion,"nacimiento":nacimiento,"altura":altura,"peso":peso}
        current_index= self.lista.currentRow()
        self.usersArr[current_index]= user_editado
        #actualiza la base de datos
        current_user_id = self.current_user["id"]
        self.cursor.execute(f"UPDATE usuarios SET nombre='{nombre}',apellido='{apellido}',mail='{mail}',telefono='{telefono}',direccion='{direccion}',nacimiento='{nacimiento}',altura='{altura}',peso='{peso}' WHERE id='{current_user_id}'")
        self.conexion.commit()
        #actualiza el nombre
        self.lista.currentItem().setText(f"{nombre} {apellido}")
        
        #habilita los botones
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.set_readOnlyInputs(True)
        self.confirm_panel_edit.hide()
    
    def on_cancelar_edit(self):
        self.set_readOnlyInputs(True)
        self.confirm_panel_edit.hide()
        self.confirm_panel_nuevo.hide()
        self.nuevo.setEnabled(True)
        self.eliminar.setEnabled(True)
        #coloca los valores nuevamente
        current_index= self.lista.currentRow()
        current_user = self.usersArr[current_index]
        self.fill_user(current_user)
        
        
    #funcionalidad para eliminar
    
    def on_eliminar(self):
        self.confirm_panel_nuevo.hide()
        self.confirm_panel_edit.hide()
        item_actual=self.lista.currentItem()
        #crea mensaje
        msg = QMessageBox()
        msg.setWindowTitle("Elimar usuario")
        msg.setText(f"Realmente desea eliminar a {item_actual.text()}")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No )
        resultado = msg.exec()
        #toma de decisiones segun resultado
        if resultado == QMessageBox.Yes:
            #encuentra al usuario
            current_user_index = self.current_user["id"]
            self.cursor.execute(f"DELETE FROM usuarios WHERE id='{current_user_index}'")
            self.conexion.commit()
            self.lista.takeItem(self.lista.currentRow())
            #elimina el ususario del arr
            self.usersArr.remove(self.current_user)
            self.form.hide()
            self.editar.setEnabled(False)
            self.eliminar.setEnabled(False)
        if resultado == QMessageBox.No:
            pass
        
        
        
        
    
        
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

