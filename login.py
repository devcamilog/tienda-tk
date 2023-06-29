#importar la libreria
import sqlite3
import sys
from subprocess import call 
from tkinter import *
from tkinter import messagebox 
#importar libreria para el manejo de imagenes
from PIL import ImageTk, Image

#definimos la clase

class Login:
    
    db_name = 'bd_proyecto_2560152.db'
    
    #constructor de la clase
    def __init__(self,ventana_login):
        '''------------ Atributos de la ventana ------------'''
        self.window = ventana_login
        #Titulo a la ventana
        self.window.title("Ingreso al Sistema")
        #Tamaño de la ventana
        self.window.geometry("430x470")
        #Incluir un icono a la ventana 
        self.window.iconbitmap("Icon.ico")
        #Modificar o no las dimensiones de la ventana
        self.window.resizable(0,0)
        #color de ventana 
        self.window.config(bd=10)
        
        '''------------ Titulo de la ventana ------------'''
        titulo = Label(ventana_login, text="INICIAR SESION", fg="black", font=("Comic Sans MS", 13,"bold"), pady=10).pack()
        
        '''------------ Logo de la ventana ------------'''
        #Cargamos la imagen
        imagen_login = Image.open("logo.png")
        #Tamaño de la imagen
        nueva_imagen = imagen_login.resize((40,40))
        #renderizamos las caracteristicas de la imagen
        render = ImageTk.PhotoImage(nueva_imagen)
        #label para cargar la imagen
        label_imagen = Label(ventana_login, image=render)
        #renderizo el label
        label_imagen.image = render
        #empaqueto y ubicamos
        label_imagen.pack(pady=5)
        
        '''------------ Marco de la ventana ------------'''
        marco = LabelFrame(ventana_login, text="Ingre sus datos",font=("Comic Sans MS", 10,"bold"))
        marco.pack()
        
        '''------------ Formulario de la ventana ------------'''
        label_usuario = Label(marco,text="Usuario: ", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.usuario = Entry(marco, width=25)
        #focus ubica el cursor en el Entry
        self.usuario.focus()
        self.usuario.grid(row=0, column=1, padx=5, pady=10)

        label_password = Label(marco, text="Password: ", font=("Comic Sans MS", 10, "bold")).grid(row=1, column=0, sticky='s', padx=5, pady=10)
        #show muestra asteriscos
        self.password = Entry(marco, show="*")
        self.password.grid(row=1, column=1, padx=5, pady=10)
        
        '''------------ Frame de Botones de la ventana ------------'''
        frame_botones = Frame(ventana_login)
        frame_botones.pack()
        
        '''------------ Botones de la ventana ------------'''
        boton_ingresar = Button(frame_botones, text="INGRESAR",command=self.login,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=0, padx=10, pady=15)
        boton_registrar = Button(frame_botones, text="REGISTRAR",command=self.llamar_registro, height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        label_recuperar = Label(frame_botones, text="¿Olvidaste tu contraseña? ", font=("Comic Sans MS", 10, "bold")).grid(row=1, column=0, columnspan=2, sticky='s')
        boton_recuperar = Button(frame_botones, text="RECUPERAR", command=self.llamar_recuperar,height=1, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=2, column=0, columnspan=2, padx=10, pady=8)
        
    def llamar_registro(self):
        ventana_login.destroy()
        call([sys.executable, 'registro.py'])
    
    def llamar_recuperar(self):
        ventana_login.destroy()
        call([sys.executable, 'recuperar.py'])
    
    def login(self):
        if (self.validar_formulario_completo()):
            usuario = self.usuario.get()
            password = self.password.get()
            dato = self.validar_login(usuario, password)
            if(dato != []):
                messagebox.showinfo("Bienvenido/a", "Datos ingresados correctamente")
                
                self.productos()
            else:
                messagebox.showerror("ERROR DE INGRESO", "Usuario o contraseña incorrectos")
                    
    def validar_formulario_completo(self):
        if len(self.usuario.get())!= 0 and len(self.password.get())!=0:
            return True
        else:
            messagebox.showerror("ERROR DE INGRESO", "Ingrese el formulario completo")
            
    def productos(self):
        ventana_login.destroy()
        call([sys.executable, 'productos.py'])
    
    def validar_login(self,usuario,password):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            query = f"SELECT * FROM Usuarios WHERE usuario='{usuario}' AND contrasena='{password}'"
            cursor.execute(query)
            validacion = cursor.fetchall()
            cursor.close()
            return validacion
            
            
            
if __name__=='__main__':
    ventana_login = Tk()
    application = Login(ventana_login)
    ventana_login.mainloop()        