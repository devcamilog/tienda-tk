from tkinter import messagebox 
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

import sys
from subprocess import call
import sqlite3


class Login:
    db_name='bd_proyecto_2560152.db'
    #constructor de la clase
    def __init__(self,ventana_productos):
        pass
        '''--------------Atributos de la ventana----------------'''
        menubar = Menu(ventana_productos)
        
        # self.window = ventana_productos
        # #titulo a la ventana
        # self.window.title("PRODUCTOS")
        # #tamaño de la venta
        # self.window.geometry("1100x700")
        # #incluir un icono a la ventana
        # self.window.iconbitmap("Imagen.ico")
        # #modificar o no las dimensiones de la ventana
        # self.window.resizable(0,0)
        # #icono de ventana
        # self.window.config(bd=10)
        
        '''---------------Titulo de la ventana------------------'''
        titulo = Label(ventana_productos, text="LISTA DE CLIENTES", fg="black",font=("Comic Sans MS",13, "bold"), pady=10).pack()
        
        '''--------------FRAME DE LOS PRODUCTOS--------------------'''
        
        frame_imagen = Frame(ventana_productos)
        frame_imagen.pack()
        
        #imagenes
        # imagen_gafas = Image.open("gafas-de-sol.png")
        # nueva_imagen = imagen_gafas.resize((40,40))
        # render = ImageTk.PhotoImage(nueva_imagen)
        # label_imagen = Label(frame_imagen, image=render)
        # label_imagen.image = render
        # label_imagen.grid(row=0,column=1,padx=10,pady=5)


        # imagen_camiseta = Image.open("camiseta-de-manga-corta.png")
        # nueva_imagen = imagen_camiseta.resize((40,40))
        # render = ImageTk.PhotoImage(nueva_imagen)
        # label_imagen = Label(frame_imagen, image=render)
        # label_imagen.image = render
        # label_imagen.grid(row=0,column=2,padx=10,pady=5)

        
        # imagen_gorra = Image.open("gorra.png")
        # nueva_imagen = imagen_gorra.resize((40,40))
        # render = ImageTk.PhotoImage(nueva_imagen)
        # label_imagen = Label(frame_imagen, image=render)
        # label_imagen.image = render
        # label_imagen.grid(row=0,column=3,padx=10,pady=5)

        # imagen_buso = Image.open("buso.png")
        # nueva_imagen = imagen_buso.resize((40,40))
        # render = ImageTk.PhotoImage(nueva_imagen)
        # label_imagen = Label(frame_imagen, image=render)
        # label_imagen.image = render
        # label_imagen.grid(row=0,column=4,padx=10,pady=5)
        
        
        '''---------------Marco de la ventana ------------------'''
        marco = LabelFrame(ventana_productos, text="Informacion del cliente", font=("Comic Sans MS", 10, "bold"))
        marco.pack()
        
        '''---------------Formulario de la ventana ------------------'''
        label_codigo_cliente = Label(marco, text="ID cliente: ",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0,sticky='s', padx=5, pady=10)
        self.codigo_cliente = Entry(marco,width=25)
        self.codigo_cliente.focus()
        self.codigo_cliente.grid(row=0, column=1, padx=5, pady=10)

        label_nombre_cliente = Label(marco, text="Nombres: ",font=("Comic Sans MS", 10, "bold")).grid(row=1, column=0,sticky='s', padx=5, pady=10)
        self.nombre_cliente = Entry(marco,width=25)
        self.nombre_cliente.focus()
        self.nombre_cliente.grid(row=1, column=1, padx=5, pady=10)

        label_apellido_cliente = Label(marco, text="Apellidos: ",font=("Comic Sans MS", 10, "bold")).grid(row=2, column=0,sticky='s', padx=5, pady=10)
        self.apellido_cliente = Entry(marco,width=25)
        self.apellido_cliente.focus()
        self.apellido_cliente.grid(row=2, column=1, padx=5, pady=10)

        label_correo_cliente = Label(marco, text="Correo ",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=2,sticky='s', padx=5, pady=10)
        self.correo_cliente = Entry(marco,width=25)
        self.correo_cliente.focus()
        self.correo_cliente.grid(row=0, column=3, padx=5, pady=10)

        
        label_telefono_cliente = Label(marco, text="Telefono: ",font=("Comic Sans MS", 10, "bold")).grid(row=1, column=2,sticky='s', padx=5, pady=10)
        self.telefono_cliente = Entry(marco,width=25)
        self.telefono_cliente.focus()
        self.telefono_cliente.grid(row=1, column=3, padx=5, pady=10)

        label_cedula_cliente = Label(marco, text="Cedula: ",font=("Comic Sans MS", 10, "bold")).grid(row=2, column=2,sticky='s', padx=5, pady=10)
        self.cedula_cliente = Entry(marco,width=25)
        self.cedula_cliente.focus()
        self.cedula_cliente.grid(row=2, column=3, padx=5, pady=10)

        '''---------------Frame botones de la ventana ------------------'''
        frame_botones = Frame(ventana_productos)
        frame_botones.pack()

        '''------------------- botones de la ventana ------------------'''
        boton_registrar = Button(frame_botones, text="REGISTRAR",command=self.agregar_cliente,height=2,width=12, bg="Blue", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0,padx=10,pady=15)
        boton_editar = Button(frame_botones, text="EDITAR",command=self.editar_cliente,height=2,width=12, bg="orange", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=1,padx=10,pady=15)
        boton_eliminar = Button(frame_botones, text="ELIMINAR",command=self.eliminar_cliente,height=2,width=12, bg="red", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=2,padx=10,pady=15)
        boton_salir = Button(frame_botones, text="SALIR",command=self.cerrarVentana,height=2,width=12, bg="green", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=3,padx=10,pady=15)

        '''---------------Frame botones de la ventana ------------------'''
        frame_botonesRP = Frame(ventana_productos)
        frame_botonesRP.pack()
        
        '''---------------Tabla con la lista de los productos ------------------'''
        self.tree = ttk.Treeview(height=13,columns=("columna1","columna2","columna3","columna4","columna5"))
        self.tree.heading("#0", text='Codigo Cliente', anchor=CENTER)
        self.tree.column("#0", width=90, minwidth=75, stretch=False)
        
        self.tree.heading("columna1",text='Nombre', anchor=CENTER)
        self.tree.column("columna1", width=150, minwidth=75, stretch=False)

        self.tree.heading("columna2",text='Apellido', anchor=CENTER)
        self.tree.column("columna2", width=150, minwidth=75, stretch=False)

        self.tree.heading("columna3",text='Correo', anchor=CENTER)
        self.tree.column("columna3", width=150, minwidth=75, stretch=False)

        self.tree.heading("columna4",text='Telefono', anchor=CENTER)
        self.tree.column("columna4", width=150, minwidth=75, stretch=False)

        self.tree.heading("columna5",text='Cedula', anchor=CENTER)
        self.tree.column("columna5", width=150, minwidth=75, stretch=False)
        

        self.tree.pack()
    
        self.listar_cliente()
        

    def agregar_cliente(self):
        if self.validar_formulario() and self.validar_cliente():
            query = 'INSERT INTO Productos VALUES(NULL, ? , ? , ?, ?, ? , ?)' 
            parameters = (self.codigo_cliente.get(),self.nombre_cliente.get(),self.apellido_cliente.get(),self.correo_cliente.get(),self.telefono_cliente.get(),self.cedula_cliente.get())
            self.ejecutar_consulta(query,parameters)
            messagebox.showinfo("REGISTRO EXITOSO", "Agregaste un producto")
            self.limpiar_formulario()
            self.listar_cliente()
    
    def validar_formulario(self):
        if len(self.codigo_cliente.get()) !=0 and len(self.nombre_cliente.get()) !=0 and len(self.apellido_cliente.get()) !=0 and len(self.correo_cliente.get()) !=0 and len(self.telefono_cliente.get()) !=0 and len(self.cedula_cliente.get()) !=0 :
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "Complete todos los campos del formulario")

    def ejecutar_consulta(self, query, parameters=()):
        #conexion a la bd
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            #se realiza la ejecucion de la sentencia SQL que llega en el query y los parametros
            result = cursor.execute(query,parameters)
            # se hace el committ de la sentencia SQL
            conexion.commit()
        #se retorna el resultado de la ejecucion de la sentencia SQL
        return result

    def validar_cliente(self):
        #se obtiene el atributo producto del formulario y se almacena en la variable producto
        codigo = self.codigo_cliente.get()
        #se invoca el metodo buscar producto y se envia el producto ingresado en el formulario
        #lo que retorne el metodo se almacena en la variable dato
        dato = self.buscar_cliente(codigo)
        #si el metodo buscar_cliente devuelve a dato una cadena vacia es porque el dni no existe
        if (dato == []):
            return True
        else:
            #se crea una ventana de error si el producto ya existe en la bd
            messagebox.showerror("ERROR EN REGISTRO", " producto registrado anteriormente")
            
    def buscar_cliente(self, producto):
        #conexion SQL
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            #consulta SQL FORMAT(producto) es el producto que se ingreso al formulario
            sql = "SELECT * FROM Productos WHERE nombre = {}".format(producto)
            #ejecucion de la consulta sql
            cursor.execute(sql)
            producto_consulta = cursor.fetchall() # obtener respuesta como lista
            # se realiza el cierre de la conexion con la bd
            cursor.close()
            #se retorna la consulta
            return producto_consulta
     
    def limpiar_formulario(self):
        self.codigo_cliente.delete(0, END)
        self.nombre_cliente.delete(0, END)
        self.apellido_cliente.delete(0, END)
        self.correo_cliente.delete(0, END)
        self.cedula_cliente.delete(0, END)
        self.telefono_cliente.delete(0, END)
           
    def cerrarVentana(self):
        ventana_productos.destroy()
        
    def listar_cliente(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        query = 'SELECT * FROM Productos ORDER BY nombre DESC'
        db_rows = self.ejecutar_consulta(query)
        for row in db_rows:
            self.tree.insert("",0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))

    def eliminar_cliente(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            messagebox.showerror("ERROR", "Debe seleccionar un producto de la tabla")
        dato = self.tree.item(self.tree.selection())['text']
        nombre = self.tree.item(self.tree.selection())['values'][0]
        query = "DELETE FROM Productos WHERE codigo = ?"
        respuesta = messagebox.askquestion("ADVERTENCIA", f"¿?Esta seguro que desea eliminar el producto: {nombre}?")
        if respuesta == 'yes':
            self.ejecutar_consulta(query,(dato,))
            self.listar_cliente()
            messagebox.showinfo('EXITO',f'Producto elminado: {nombre}')
        else:
            messagebox.showerror('ERROR', f'Error al eliminar el producto: {nombre}')

    def editar_cliente(self):
            try:
                self.tree.item(self.tree.selection())['values'][0]
            except IndexError as e:
                messagebox.showerror("ERROR", "Debe seleccionar un producto de la tabla")

            codigo_cliente = self.tree.item(self.tree.selection())['text']
            nombre = self.tree.item(self.tree.selection())['values'][0]
            apellido = self.tree.item(self.tree.selection())['values'][1]
            correo = self.tree.item(self.tree.selection())['values'][2]
            cedula = self.tree.item(self.tree.selection())['values'][3]
            telefono = self.tree.item(self.tree.selection())['values'][4]

            self.ventana_editar = Toplevel()
            self.ventana_editar.title("EDITAR PRODUCTO")
            #incluir un icono a la ventana
            self.ventana_editar.iconbitmap("Imagen.ico")
            #modificar o no las dimensiones de la ventana
            self.ventana_editar.resizable(0,0)

            label_codigo_cliente = Label(self.ventana_editar, text="Id cliente:", font=("Comic Sans", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=8)
            nuevo_codigo_cliente = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=codigo_cliente), width=25)
            nuevo_codigo_cliente.grid(row=0, column=1, padx=5, pady=8)

            label_nombre = Label(self.ventana_editar, text="Nombres :", font=("Comic Sans", 10, "bold")).grid(row=1, column=0, sticky='s', padx=5, pady=8)
            nuevo_nombre = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=nombre), width=25)
            nuevo_nombre.grid(row=1, column=1, padx=5, pady=0)

            label_apellido = Label(self.ventana_editar, text="Apellidos:", font=("Comic Sans", 10, "bold")).grid(row=2, column=0, sticky='s', padx=5, pady=8)
            nuevo_apellido = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=apellido), width=25)
            nuevo_apellido.grid(row=2, column=1, padx=5, pady=0)

            label_correo = Label(self.ventana_editar, text="Correo:", font=("Comic Sans", 10, "bold")).grid(row=0, column=2, sticky='s', padx=5, pady=8)
            nuevo_combo_correo = ttk.Combobox(self.ventana_editar, values=["Gafas", "Ropa", "Gorra"], width=22, state="readonly")
            nuevo_combo_correo.set(correo)
            nuevo_combo_correo.grid(row=0, column=3, padx=5, pady=0)


            label_telefono = Label(self.ventana_editar, text="Telefono:", font=("Comic Sans", 10, "bold")).grid(row=1, column=2, sticky='s', padx=5, pady=8)
            nueva_telefono = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=telefono), width=25)
            nueva_telefono.grid(row=2, column=3, padx=5, pady=0)

            label_cedula = Label(self.ventana_editar, text="Cedula:", font=("Comic Sans", 10, "bold")).grid(row=2, column=2, sticky='s', padx=5, pady=8)
            nuevo_cedula = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=cedula), width=25)
            nuevo_cedula.grid(row=1, column=3, padx=5, pady=0)

            boton_actualizar = Button(self.ventana_editar, text="ACTUALIZAR", command=lambda:self.actualizar(nuevo_codigo_cliente.get(), nuevo_nombre.get(), nuevo_apellido.get(), nuevo_combo_correo.get(), label_telefono.get(), nuevo_cedula.get(), codigo_cliente), height=2, width=20, bg="blue", fg="white", font=("Comic Sans MS", 9, "bold"))
            boton_actualizar.grid(row=3, column=1, columnspan=2, padx=10, pady=15)

            self.ventana_editar.mainloop()

  
if __name__ == '__main__':
    ventana_productos = Tk() 
    application = Login(ventana_productos)
    ventana_productos.mainloop()    