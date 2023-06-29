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
    def __init__(self,ventana_ventas):
        pass
        '''--------------Atributos de la ventana----------------'''
        menubar = Menu(ventana_ventas)
        
        # self.window = ventana_ventas
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
        titulo = Label(ventana_ventas, text="LISTA DE VENTAS", fg="black",font=("Comic Sans MS",13, "bold"), pady=10).pack()
        
        '''--------------FRAME DE LOS PRODUCTOS--------------------'''
        
        frame_imagen = Frame(ventana_ventas)
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
        marco = LabelFrame(ventana_ventas, text="Informacion de las ventas", font=("Comic Sans MS", 10, "bold"))
        marco.pack()
        
        '''---------------Formulario de la ventana ------------------'''
        label_codigo_venta = Label(marco, text="ID venta: ",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0,sticky='s', padx=5, pady=10)
        self.codigo_venta = Entry(marco,width=25)
        self.codigo_venta.focus()
        self.codigo_venta.grid(row=0, column=1, padx=5, pady=10)

        label_codigo_articulo = Label(marco, text="codigo articulo: ",font=("Comic Sans MS", 10, "bold")).grid(row=1, column=0,sticky='s', padx=5, pady=10)
        self.codigo_articulo = Entry(marco,width=25)
        self.codigo_articulo.focus()
        self.codigo_articulo.grid(row=1, column=1, padx=5, pady=10)

        label_codigo_cliente = Label(marco, text="Codigo cliente ",font=("Comic Sans MS", 10, "bold")).grid(row=2, column=0,sticky='s', padx=5, pady=10)
        self.codigo_cliente = Entry(marco,width=25)
        self.codigo_cliente.focus()
        self.codigo_cliente.grid(row=2, column=1, padx=5, pady=10)

        label_fecha = Label(marco, text="Fecha",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=2,sticky='s', padx=5, pady=10)
        self.fecha_venta = Entry(marco,width=25)
        self.fecha_venta.focus()
        self.fecha_venta.grid(row=0, column=3, padx=5, pady=10)

        


        '''---------------Frame botones de la ventana ------------------'''
        frame_botones = Frame(ventana_ventas)
        frame_botones.pack()

        '''------------------- botones de la ventana ------------------'''
        boton_registrar = Button(frame_botones, text="AGREGAR",command=self.agregar_venta,height=2,width=12, bg="Blue", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0,padx=10,pady=15)
        boton_editar = Button(frame_botones, text="EDITAR",command=self.editar_venta,height=2,width=12, bg="orange", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=1,padx=10,pady=15)
        boton_eliminar = Button(frame_botones, text="ELIMINAR",command=self.eliminar_venta,height=2,width=12, bg="red", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=2,padx=10,pady=15)
        boton_salir = Button(frame_botones, text="SALIR",command=self.cerrarVentana,height=2,width=12, bg="green", fg="white",font=("Comic Sans MS", 10, "bold")).grid(row=0, column=3,padx=10,pady=15)

        '''---------------Frame botones de la ventana ------------------'''
        frame_botonesRP = Frame(ventana_ventas)
        frame_botonesRP.pack()
        
        '''---------------Tabla con la lista de los productos ------------------'''
        self.tree = ttk.Treeview(height=13,columns=("columna1","columna2","columna3"))
        self.tree.heading("#0", text='ID VENTA', anchor=CENTER)
        self.tree.column("#0", width=90, minwidth=75, stretch=False)
        
        self.tree.heading("columna1",text='Codigo Articulo:', anchor=CENTER)
        self.tree.column("columna1", width=150, minwidth=75, stretch=False)

        self.tree.heading("columna2",text='Codigo  Cliente', anchor=CENTER)
        self.tree.column("columna2", width=150, minwidth=75, stretch=False)

        self.tree.heading("columna3",text='Fecha', anchor=CENTER)
        self.tree.column("columna3", width=150, minwidth=75, stretch=False)

        self.tree.pack()
    
        self.listar_ventas()
        
    def agregar_venta(self):
        if self.validar_formulario() and self.validar_cliente():
            query = 'INSERT INTO Ventas VALUES(?,?,? , ? )' 
            parameters = (self.codigo_venta.get(),self.codigo_articulo.get(),self.codigo_cliente.get(),self.fecha_venta.get())
            self.ejecutar_consulta(query,parameters)
            messagebox.showinfo("REGISTRO EXITOSO", "Agregaste una venta")
            self.limpiar_formulario()
            self.listar_ventas()
    
    def validar_formulario(self):
        if len(self.codigo_venta.get()) !=0 and len(self.codigo_articulo.get()) !=0 and len(self.codigo_cliente.get()) !=0 and len(self.fecha_venta.get()) !=0 :
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

    def validar_venta(self):
        #se obtiene el atributo producto del formulario y se almacena en la variable producto
        codigo = self.codigo_venta.get()
        #se invoca el metodo buscar producto y se envia el producto ingresado en el formulario
        #lo que retorne el metodo se almacena en la variable dato
        dato = self.buscar_venta(codigo)
        #si el metodo buscar_venta devuelve a dato una cadena vacia es porque el dni no existe
        if (dato == []):
            return True
        else:
            #se crea una ventana de error si el producto ya existe en la bd
            messagebox.showerror("ERROR EN REGISTRO", " venta registrada anteriormente")

    def validar_cliente(self):
        #se obtiene el atributo producto del formulario y se almacena en la variable producto
        codigo1 = self.codigo_cliente.get()
        codigo2 = self.codigo_articulo.get()
        #se invoca el metodo buscar producto y se envia el producto ingresado en el formulario
        #lo que retorne el metodo se almacena en la variable dato
        dato1 = self.buscar_cliente(codigo1)
        dato2 = self.buscar_producto(codigo2)
        #si el metodo buscar_venta devuelve a dato una cadena vacia es porque el dni no existe
        if (dato1 == [] and dato2 == []):
            messagebox.showerror("ERROR EN REGISTRO", " el producto y el cliente no existe")
        elif(dato1 == []):
            messagebox.showerror("ERROR EN REGISTRO", "  El cliente no existe")
        elif(dato2 == []):
            messagebox.showerror("ERROR EN REGISTRO", "  El producto no existe")
        else:
            #se crea una ventana de error si el producto ya existe en la bd
            return True            
        

    # def validar_producto(self):
    #     #se obtiene el atributo producto del formulario y se almacena en la variable producto
    #     #se invoca el metodo buscar producto y se envia el producto ingresado en el formulario
    #     #lo que retorne el metodo se almacena en la variable dato
    #     #si el metodo buscar_venta devuelve a dato una cadena vacia es porque el dni no existe
    #     if (dato == []):
    #         messagebox.showerror("ERROR EN REGISTRO", " producto no existe")
    #     else:
    #         #se crea una ventana de error si el producto ya existe en la bd
    #         return True        

    def buscar_venta(self, venta):
        #conexion SQL
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            #consulta SQL FORMAT(cliente) es el cliente que se ingreso al formulario
            sql = "SELECT * FROM Ventas WHERE id = {}".format(venta)
            #ejecucion de la consulta sql
            cursor.execute(sql)
            producto_consulta = cursor.fetchall() # obtener respuesta como lista
            # se realiza el cierre de la conexion con la bd
            cursor.close()
            #se retorna la consulta
            return producto_consulta

    def buscar_cliente(self, cliente):
        #conexion SQL
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            #consulta SQL FORMAT(cliente) es el cliente que se ingreso al formulario
            sql = "SELECT * FROM Clientes WHERE codigo = {}".format(cliente)
            #ejecucion de la consulta sql
            cursor.execute(sql)
            producto_consulta = cursor.fetchall() # obtener respuesta como lista
            # se realiza el cierre de la conexion con la bd
            cursor.close()
            #se retorna la consulta
            return producto_consulta

    def buscar_producto(self, producto):
        #conexion SQL
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            #consulta SQL FORMAT(producto) es el producto que se ingreso al formulario
            sql = "SELECT * FROM Productos WHERE codigo = {}".format(producto)
            #ejecucion de la consulta sql
            cursor.execute(sql)
            producto_consulta = cursor.fetchall() # obtener respuesta como lista
            # se realiza el cierre de la conexion con la bd
            cursor.close()
            #se retorna la consulta
            return producto_consulta
     
    def limpiar_formulario(self):
        self.codigo_venta.delete(0, END)
        self.codigo_articulo.delete(0, END)
        self.codigo_cliente.delete(0, END)
        self.fecha_venta.delete(0, END)
      
    def cerrarVentana(self):
        ventana_ventas.destroy()
        
    def listar_ventas(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        query = 'SELECT * FROM Ventas ORDER BY id DESC'
        db_rows = self.ejecutar_consulta(query)
        for row in db_rows:
            self.tree.insert("",0, text=row[0], values=(row[1], row[2], row[3]))

    def eliminar_venta(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            messagebox.showerror("ERROR", "Debe seleccionar un producto de la tabla")
        dato = self.tree.item(self.tree.selection())['text']
        nombre = self.tree.item(self.tree.selection())['values'][0]
        query = "DELETE FROM Ventas WHERE id = ?"
        respuesta = messagebox.askquestion("ADVERTENCIA", f"¿?Esta seguro que desea eliminar la venta: {nombre}?")
        if respuesta == 'yes':
            self.ejecutar_consulta(query,(dato,))
            self.listar_ventas()
            messagebox.showinfo('EXITO',f'Producto elminado: {nombre}')
        else:
            messagebox.showerror('ERROR', f'Error al eliminar el producto: {nombre}')

    def editar_venta(self):
            try:
                self.tree.item(self.tree.selection())['values'][0]
            except IndexError as e:
                messagebox.showerror("ERROR", "Debe seleccionar un producto de la tabla")

            codigo_venta = self.tree.item(self.tree.selection())['text']
            codigo_articulo = self.tree.item(self.tree.selection())['values'][0]
            codigo_cliente = self.tree.item(self.tree.selection())['values'][1]
            fecha = self.tree.item(self.tree.selection())['values'][2]
  

            self.ventana_editar = Toplevel()
            # self.ventana_editar.title("EDITAR PRODUCTO")
            # #incluir un icono a la ventana
            # self.ventana_editar.iconbitmap("Imagen.ico")
            # #modificar o no las dimensiones de la ventana
            # self.ventana_editar.resizable(0,0)

            label_codigo_venta = Label(self.ventana_editar, text="Id venta:", font=("Comic Sans", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=8)
            nuevo_codigo_venta = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=codigo_venta), width=25)
            nuevo_codigo_venta.grid(row=0, column=1, padx=5, pady=8)

            label_codigo_articulo = Label(self.ventana_editar, text="Codigo Articulo :", font=("Comic Sans", 10, "bold")).grid(row=1, column=0, sticky='s', padx=5, pady=8)
            nuevo_codigo_articulo = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=codigo_articulo), width=25)
            nuevo_codigo_articulo.grid(row=1, column=1, padx=5, pady=0)

            label_codigo_cliente = Label(self.ventana_editar, text="Codigo  Cliente:", font=("Comic Sans", 10, "bold")).grid(row=2, column=0, sticky='s', padx=5, pady=8)
            nuevo_codigo_cliente = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=codigo_cliente), width=25)
            nuevo_codigo_cliente.grid(row=2, column=1, padx=5, pady=0)

            label_fecha = Label(self.ventana_editar, text="Fecha:", font=("Comic Sans", 10, "bold")).grid(row=0, column=2, sticky='s', padx=5, pady=8)
            nueva_fecha = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=fecha), width=25)
            nueva_fecha.grid(row=0, column=3, padx=5, pady=0)

            boton_actualizar = Button(self.ventana_editar, text="ACTUALIZAR", command=lambda:self.actualizar(nuevo_codigo_venta.get(), nuevo_codigo_articulo.get(), nuevo_codigo_cliente.get(), nueva_fecha.get(), codigo_venta), height=2, width=20, bg="blue", fg="white", font=("Comic Sans MS", 9, "bold"))
            boton_actualizar.grid(row=3, column=1, columnspan=2,padx=10, pady=15)
            self.ventana_editar.mainloop()

    def actualizar(self,nuevo_codigo_venta, nuevo_codigo_articulo,nuevo_codigo_cliente,nueva_fecha,codigo_venta):
        query ='UPDATE Ventas SET id=?,codigo_producto= ?, codigo_cliente = ?,fecha = ? WHERE id = ?'
        parameters = (nuevo_codigo_venta, nuevo_codigo_articulo, nuevo_codigo_cliente, nueva_fecha, codigo_venta)
        self.ejecutar_consulta(query, parameters)
        messagebox.showinfo('EXITO', f'Venta Actualizada:{codigo_venta}')
        self.ventana_editar.destroy()
        self.listar_ventas()

if __name__ == '__main__':
    ventana_ventas = Tk() 
    application = Login(ventana_ventas)
    ventana_ventas.mainloop()    