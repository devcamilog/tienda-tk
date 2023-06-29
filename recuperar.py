from tkinter import *
import sys
from subprocess import call
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import ttk 
import sqlite3


class Recuperar:
    
    db_name = 'bd_proyecto_2560152.db'
        
    def __init__(self,ventana_recuperar):
        '''------------ Atributos de la ventana ------------'''
        self.window = ventana_recuperar
        #Titulo a la ventana
        self.window.title("RECUPERAR PASSWORD")
        #Tamaño de la ventana
        self.window.geometry("430x520")
        #Incluir un icono a la ventana 
        self.window.iconbitmap("Icon.ico")
        #Modificar o no las dimensiones de la ventana
        self.window.resizable(0,0)
        #color de ventana 
        self.window.config(bd=10)
    
        '''------------ Titulo de la ventana ------------'''
        titulo = Label(ventana_recuperar, text="RECUPERAR PASSWORD", fg="black", font=("Comic Sans MS", 13,"bold"), pady=10).pack()
        
        '''------------ Logo de la ventana ------------'''
        #Cargamos la imagen
        imagen_login = Image.open("password1.png")
        #Tamaño de la imagen
        nueva_imagen = imagen_login.resize((40,40))
        #renderizamos las caracteristicas de la imagen
        render = ImageTk.PhotoImage(nueva_imagen)
        #label para cargar la imagen
        label_imagen = Label(ventana_recuperar, image=render)
        #renderizo el label
        label_imagen.image = render
        #empaqueto y ubicamos
        label_imagen.pack(pady=5)

        '''------------ Marco de la ventana ------------'''
        marco = LabelFrame(ventana_recuperar, text="Datos de recuperacion del password",font=("Comic Sans MS", 10,"bold"))
        marco.pack()
        
        '''------------ Formulario de la ventana ------------'''
        label_usuario= Label(marco,text="Usuario: ", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=10)
        self.usuario = Entry(marco, width=25)
        self.usuario.focus()
        self.usuario.grid(row=0, column=1, padx=5, pady=10)
        
        label_info = Label(marco, text="Seleccione una pregunta y digite la respuesta correcta", fg="red",font=("Comic Sans MS", 10, "bold")).grid(row=1, column=0, columnspan=2, sticky='s', padx=5, pady=10)
        
        label_pregunta = Label(marco,text="Preguntas:", font=("Comic Sans MS", 10, "bold")).grid(row=2, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.combo_pregunta = ttk.Combobox(marco, values=["Tipo de sangre", "Correo electronico de recuperacion", "Telefono de recuperacion", "Nombre de la primera mascota"], width=22, state="readonly")
        self.combo_pregunta.current(0)
        self.combo_pregunta.grid(row=2, column=1, padx=10, pady=8)
        
        label_respuesta = Label(marco,text="Respuesta: ", font=("Comic Sans MS", 10, "bold")).grid(row=3, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.respuesta = Entry(marco, width=25)
        self.respuesta.grid(row=3, column=1, padx=5, pady=10)
        
        label_nuevo_password = Label(marco, text="Password: ", font=("Comic Sans MS", 10, "bold")).grid(row=4, column=0, sticky='s', padx=5, pady=10)
        #show muestra asteriscos
        self.password = Entry(marco, show="*")
        self.password.grid(row=4, column=1, padx=5, pady=10)
        
        label_repetir_password = Label(marco,text="Confirmar Password: ", font=("Comic Sans MS", 10, "bold")).grid(row=5, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.repetir_password = Entry(marco, show="*")
        self.repetir_password.grid(row=5, column=1, padx=5, pady=10)
        
        '''------------ Frame de Botones de la ventana ------------'''
        frame_botones = Frame(ventana_recuperar)
        frame_botones.pack()

        '''------------ Botones de la ventana ------------'''
        boton_recuperar = Button(frame_botones, text="RECUPERAR", command=self.restablecer_password,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=1, column=0, padx=10, pady=15)
        boton_login = Button(frame_botones, text="LOGIN", command=self.llamar_login,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=1, column=1, padx=10, pady=15)
        boton_cancelar = Button(frame_botones, text="CANCELAR",command=self.cerrarVentana,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=1, column=2, padx=10, pady=15)
        
    def cerrarVentana(self):
        ventana_recuperar.destroy()

    def llamar_login(self):
        ventana_recuperar.destroy()
        call([sys.executable, 'login.py'])
    
    def validar_formulario_completo(self):
        if len(self.usuario.get())!= 0 and len(self.password.get())!=0 and len(self.repetir_password.get())!= 0:
            return True
        else:
            messagebox.showerror("ERROR DE INGRESO", "Ingrese el formulario completo")
    
    def validar_password (self): 
        if(str(self.password.get()) == str(self.repetir_password.get())):
            return True
        else:

            messagebox.showerror("ERROR EN REGISTRO" "Contraseñas no coinciden")
    
    def ejecutar_consulta (self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            result = cursor.execute(query, parameters)
            conexion.commit()
        return result

    def restablecer_password(self):
        if self.validar_formulario_completo() and self.validar_datos_usuarios() and self.validar_password():
            query = 'UPDATE Usuarios SET contrasena =(?) WHERE usuario=(?)'
            parameters = (self.password.get(), self.usuario.get())
            self.ejecutar_consulta(query,parameters)
            messagebox.showinfo("CONTRASEÑA RECUPERADA", f'Contraseña actualizada')
            self.limpiar_formulario()
    
    def validar_datos_usuarios(self):
        usuario = self.usuario.get()
        respuesta = self.respuesta.get()
        busqueda = self.buscar_usuario(usuario, respuesta)
        if (busqueda != []):
            return True
        else:
            messagebox.showerror("ERROR DE RECUPERACION","Datos de recuperacion incorrectos")

    def buscar_usuario(self, usuario, respuesta):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            query = f"SELECT * FROM Usuarios WHERE usuario={usuario} AND respuesta='{respuesta}'"
            cursor.execute(query)
            busqueda = cursor.fetchall()
            cursor.close()
            return busqueda

    def limpiar_formulario(self):
        self.usuario.delete(0, END)
        self.password.delete(0, END)
        self.repetir_password.delete(0, END)
        self.combo_pregunta.delete(0, END)
        self.respuesta.delete(0, END)

if __name__=='__main__':
    ventana_recuperar = Tk()
    application = Recuperar(ventana_recuperar)
    ventana_recuperar.mainloop()  