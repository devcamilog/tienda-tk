#importar la libreria
import sys
from subprocess import call 
import sqlite3
from tkinter import *
from tkinter import messagebox 
#importar libreria para el manejo de imagenes
from PIL import ImageTk, Image
from tkinter import ttk 

#definimos la clase

class Registro:
    #bd del proyecto
    db_name='bd_proyecto_2560152.db'
    #constructor de la clase
    def __init__(self,ventana_registro):
        '''------------ Atributos de la ventana ------------'''
        self.window = ventana_registro
        #Titulo a la ventana
        self.window.title("Registro al sistema")
        #Tamaño de la ventana
        self.window.geometry("430x870")
        #Incluir un icono a la ventana 
        self.window.iconbitmap("Icon.ico")
        #Modificar o no las dimensiones de la ventana
        self.window.resizable(0,0)
        #color de ventana 
        self.window.config(bd=10)
        
        
        '''------------ Titulo de la ventana ------------'''
        titulo = Label(ventana_registro, text="FORMULARIO DE REGISTRO", fg="black", font=("Comic Sans MS", 13,"bold"), pady=10).pack()
        
        '''------------ Logo de la ventana ------------'''
        #Cargamos la imagen
        imagen_login = Image.open("logo.png")
        #Tamaño de la imagen
        nueva_imagen = imagen_login.resize((40,40))
        #renderizamos las caracteristicas de la imagen
        render = ImageTk.PhotoImage(nueva_imagen)
        #label para cargar la imagen
        label_imagen = Label(ventana_registro, image=render)
        #renderizo el label
        label_imagen.image = render
        #empaqueto y ubicamos
        label_imagen.pack(pady=5)
        
        '''------------ Marco de la ventana ------------'''
        marco = LabelFrame(ventana_registro, text="Ingre sus datos",font=("Comic Sans MS", 10,"bold"))
        marco.pack()
        
        '''------------ Formulario de la ventana ------------'''
        label_registro_usuario = Label(marco,text="Usuario: ", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.usuario = Entry(marco, width=25)
        #focus ubica el cursor en el Entry
        self.usuario.focus()
        self.usuario.grid(row=0, column=1, padx=5, pady=10)
        
        label_nombre = Label(marco,text="Nombre: ", font=("Comic Sans MS", 10, "bold")).grid(row=1, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.nombre = Entry(marco, width=25)
        self.nombre.grid(row=1, column=1, padx=5, pady=10)
        
        label_apellidos = Label(marco,text="Apellido: ", font=("Comic Sans MS", 10, "bold")).grid(row=2, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.apellido = Entry(marco, width=25)
        self.apellido.grid(row=2, column=1, padx=5, pady=10)
        
        label_genero = Label(marco,text="Genero: ", font=("Comic Sans MS", 10, "bold")).grid(row=3, column=0, sticky='s', padx=5, pady=10)
        self.combo_genero = ttk.Combobox(marco, values=["Masculino", "Femenino"], width=22, state="readonly")
        self.combo_genero.current(0)
        self.combo_genero.grid(row=3, column=1, padx=10, pady=10)
        
        label_edad= Label(marco,text="Edad: ", font=("Comic Sans MS", 10, "bold")).grid(row=4, column=0, sticky='s', padx=5, pady=10)
        self.edad= Entry(marco,show="")
        self.edad.grid(row=4,column=1,padx=10,pady=10)
        
        label_correo = Label(marco,text="Correo Electronico: ", font=("Comic Sans MS", 10, "bold")).grid(row=5, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.correo = Entry(marco, width=25)
        self.correo.grid(row=5, column=1, padx=5, pady=10)
        
        label_password = Label(marco, text="Password: ", font=("Comic Sans MS", 10, "bold")).grid(row=6, column=0, sticky='s', padx=5, pady=10)
        #show muestra asteriscos
        self.password = Entry(marco, show="*")
        self.password.grid(row=6, column=1, padx=5, pady=10)
        
        label_repetir_password = Label(marco,text="Confirmar Password: ", font=("Comic Sans MS", 10, "bold")).grid(row=7, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.repetir_password = Entry(marco, show="*")
        self.repetir_password.grid(row=7, column=1, padx=5, pady=10)
        
        '''------------ Marco2 de la ventana ------------'''
        marco2 = LabelFrame(ventana_registro, text="Ingre sus datos",font=("Comic Sans MS", 10,"bold"))
        marco2.pack()
        
        '''------------ Formulario de la ventana ------------'''
        label_pregunta = Label(marco2,text="Preguntas:", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.combo_pregunta = ttk.Combobox(marco2, values=["Tipo de sangre", "Correo electronico de recuperacion", "Telefono de recuperacion", "Nombre de la primera mascota"], width=22, state="readonly")
        self.combo_pregunta.current(0)
        self.combo_pregunta.grid(row=0, column=1, padx=10, pady=8)
        
        label_respuesta = Label(marco2,text="Respuesta: ", font=("Comic Sans MS", 10, "bold")).grid(row=2, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.respuesta = Entry(marco2, width=25)
        self.respuesta.grid(row=2, column=1, padx=5, pady=10)
        
        label_mensaje_password = Label(marco2,text="Esta respuesta permitira recuperar el password",fg="red", font=("Comic Sans MS",10, "bold")).grid(row=3, column=0, columnspan=2 ,padx=10, pady=15)
        
        
        '''------------ Frame de Botones de la ventana ------------'''
        frame_botones = Frame(ventana_registro)
        frame_botones.pack()

        '''------------ Botones de la ventana ------------'''
        boton_registrar = Button(frame_botones, text="REGISTRAR",command=self.registrar_usuario, height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=0, padx=10, pady=15)
        boton_limpiar = Button(frame_botones, text="LIMPIAR", command=self.limpiar_formulario, height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_login = Button(frame_botones, text="LOGIN", command=self.llamar_login,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=1, column=0, padx=10, pady=15)
        boton_cerrar = Button(frame_botones, text="CERRAR",command=self.cerrarVentana,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=1, column=1, padx=10, pady=15)

        #se crea el metodo para registrar el usuario

    def registrar_usuario(self):
        #se valida que el formulario este completo con la funcion validar formulario
        #con la funcion validar contrasena se valida que la contraseña y repetir contraseña sean iguales
        #con la funcion validar usuario se verfica que el usario no se encuentre creado en la bd
        if self.validar_formulario() and self.validar_contrasena() and self.validar_usuario():
            #consulta SQL
            #los ? representa cada campo que se va a insertar en la consulta
            query= 'INSERT INTO Usuarios VALUES (NULL,?,?,?,?,?,?,?,?)'
            #parametros que se obtienen de cada elemento definido en el formulario
            parameters = (self.usuario.get(),self.nombre.get(),self.apellido.get(),self.combo_genero.get(), self.edad.get(),self.correo.get(), self.password.get(), self.respuesta.get())
            #se invonva el metodo para enviarle la consulta y los parastros 
            self.ejecutar_consulta(query, parameters) 
            #se crea una ventana energente informativa para mostrar el mensaje de registro exitoso
            messagebox.showinfo("REGISTRO EXITOSO", f'Bienvenido {self.nombre.get()} {self.apellido.get()}')
            #se invoca el metodo limpiar formulario para que el formulario nuevamente quede vacio
            self.limpiar_formulario()        
    #se creo el metodo para validar que el formulario no tenga campos vacios

    def validar_formulario(self): #se valida que no se encuntre vacio el formulario:

        if len(self.usuario.get()) !=0 and len(self.nombre.get())  !=0 and len(self.apellido.get()) !=0 and len(self.combo_genero.get())  !=0 and len(self.edad.get())  !=0 and len(self.password.get())  !=0 and len(self.repetir_password.get()) !=0 and len(self.correo.get())  !=0 and len(self.respuesta.get())  !=0: 
            # retona True al metodo registrar usuario cuando todos los campos esten con información

            return True 
        else:
            #se crea una ventana de error si el formulario esta vacio
            messagebox.showerror("ERROR EN REGISTRO", "Complete todos los campos del formulario")
    # se crea el metodo para validar contraseña, que las contraseñas del formulario sean iguales 
    def validar_contrasena (self): 
    #se comparan que los campos de contraseña sean iguales (Que esten digitadas igual en el formulario)
    # se realiza con una comparacion de cadenas 
        if(str(self.password.get()) == str(self.repetir_password.get())):
        # retona True al metodo registrar usuario cuando los campos de contraseña son iguales 
            return True
        else:
            #se crea una ventana de error si las contraseñas no coinciden 
            messagebox.showerror("ERROR EN REGISTRO" "Contraseñas no coinciden")
    
    # se crea el metodo para validar que el usuario no exista

    def validar_usuario (self):
        #se obtiene el atributo usuario del formulario y se almacena en la variable usuario
        usuario = self.usuario.get() 
        #se invoca el metodo buscar usuario y se envia el usuario ingresado en el formulario
        #lo que retorne el metodo se almacena en la variable dato
        dato= self.buscar_usuario(usuario) 
        #si el metodo buscar_usuario devuelve a dato una cadena vacia es porque el dni no existe
        if (dato== []):
            return True
        else:
            #se crea una ventana de error si el usuario ya existe en la bd
            messagebox.showerror("ERROR EN REGISTRO", "Usuario registrado anteriormente")
        
    #se crea el metodo para verificar si el usuario existe o no en la bd 
    def buscar_usuario(self, usuario):
    #conexion SQL
        with sqlite3.connect(self.db_name) as conexion: 
            cursor = conexion.cursor()
            #consulta SQL format (usuario) es el usuario que se ingreso al formulario 
            sql = "SELECT * FROM Usuarios WHERE usuario ={}".format(usuario) 
            #ejecución de la consulta sql
            cursor.execute(sql) 
            #se realiza una consulta para validar si el usuario existe o no y se almacena en usuario consulta 
            # #si no esta el usuario se devuelve consulta vacia 
            # #fetchall devuelve contenido de la consulta en una tupla
            usuario_consulta = cursor.fetchall() # obtener respuesta como lista
            #se realiza el cierre de la conexion con la bd
            cursor.close()
            #se retorna la consulta
            return usuario_consulta
        
    #se crea el metodo para ejecutar las sentencias SQL en la bd
    def ejecutar_consulta (self, query, parameters=()):
        #conexion a la bd 
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            #se realiza la ejecucion de la sentencia SQL que llega en el query y los parametros
            result = cursor.execute(query, parameters)
            #se hace el committ de la sentencia SQL 
            conexion.commit()
        #se retorna el resultado de la ejecución de la sentencia SQL
        return result
            
            
        
    #se crea el metodo para limpiar el formulario, es decir dejarlo vacio

    def limpiar_formulario(self):

        #se limpian todos los campos vacios con el metodo delete #0, end significa que se borre el contenido desde la posicion e hasta el final del texto introducido

        self.usuario.delete(0, END)
        self.nombre.delete(0, END) 
        self.apellido.delete(0, END)
        self.combo_genero.delete(0, END)
        self.edad.delete(0, END)
        self.correo.delete(0, END) 
        self.password.delete(0, END)
        self.repetir_password.delete(0, END)
        self.combo_pregunta.delete(0, END)
        self.respuesta.delete(0, END)
    
    def cerrarVentana(self):
        ventana_registro.destroy()
        
    def llamar_login(self):
        ventana_registro.destroy()
        call([sys.executable, 'login.py'])
        
    
            
if __name__=='__main__':
    ventana_registro = Tk()
    application = Registro(ventana_registro)
    ventana_registro.mainloop()       