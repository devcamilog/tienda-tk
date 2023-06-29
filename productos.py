import sqlite3
import sys
from subprocess import call 
from tkinter import *
from tkinter import messagebox 
from tkinter import ttk 
#importar libreria para el manejo de imagenes
from PIL import ImageTk, Image

class Productos:
    #bd del proyecto
    db_name='bd_proyecto_2560152.db'
    #constructor de la clase
    def __init__(self,ventana_productos):
        '''------------ Atributos de la ventana ------------'''
           # Atributos de la ventana
        menubar = Menu(ventana_productos)
        ventana_productos.title("PRODUCTOS")
        ventana_productos.geometry("985x770")
        ventana_productos.iconbitmap("Icon.ico")
        ventana_productos.resizable(0,0)
        ventana_productos.config(bd=10, menu=menubar)
        
        
        # Menú de la ventana
        Productos_menu = Menu(menubar, tearoff=0)
        Clientes_menu = Menu(menubar, tearoff=0)
        Ventas_menu = Menu(menubar, tearoff=0)

        menubar.add_cascade(label="Productos", menu=Productos_menu)
        Informacion_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=Informacion_menu)

        menubar.add_cascade(label="Clientes", menu=Clientes_menu)
        menubar.add_cascade(label="Ventas", menu=Ventas_menu)
        
        # Iconos
        self.img_registrar = PhotoImage(file='')
        self.img_buscar = PhotoImage(file="")
        self.img_informacion = PhotoImage(file="")
        
        # Acciones de menú
        self.boton_registrar = Productos_menu.add_command(label="Registrar", command=self.widgets_crud, image=self.img_registrar, compound=LEFT)
        self.boton_buscar = Productos_menu.add_command(label="Buscar", command=self.widgets_buscador, image=self.img_buscar, compound=LEFT)
        self.boton_informacion = Informacion_menu.add_command(label="Informacion del sistema", command=self.widgets_informacion, image=self.img_informacion, compound=LEFT)
        self.boton_clientes = Clientes_menu.add_command(label="Registrar", compound=LEFT)


         # Widgets del menú
        self.label_titulo_crud = LabelFrame(ventana_productos)
        self.frame_logos_productos = LabelFrame(ventana_productos)
        self.frame_registro = LabelFrame(ventana_productos, text="Informacion del producto", font=("Comic Sans", 18, "bold"), pady=5)
        self.frame_botones_registro = LabelFrame(ventana_productos)
        self.frame_tabla_crud = LabelFrame(ventana_productos)
        
        #widgets crud 
        self.label_titulo_buscador = LabelFrame(ventana_productos)
        self.frame_buscar_producto= LabelFrame(ventana_productos, text="Buscar producto", font=("Comic Sans", 10,"bold"),pady=5)
        self.frame_boton_buscar =  LabelFrame(ventana_productos)

        self.label_informacion= LabelFrame(ventana_productos)
        #pantalla incial
        self.widgets_crud()
     
    def validar_formulario(self): #se valida que no se encuntre vacio el formulario:

        if len(self.codigo_producto.get()) !=0 and len(self.nombre_producto.get())  !=0 and len(self.cantidad.get()) !=0 and len(self.categoria.get())  !=0 and len(self.desc_producto.get())  !=0 and len(self.precio.get()) !=0:
            # retona True al metodo registrar usuario cuando todos los campos esten con información

            return True 
        else:
            #se crea una ventana de error si el formulario esta vacio
            messagebox.showerror("ERROR EN REGISTRO", "Complete todos los campos del formulario")
    
    def validar_producto (self):
        #se obtiene el atributo usuario del formulario y se almacena en la variable usuario
        codigo = self.codigo_producto.get() 
        #se invoca el metodo buscar usuario y se envia el usuario ingresado en el formulario
        #lo que retorne el metodo se almacena en la variable dato
        dato= self.buscar_producto(codigo) 
        if (dato== []):
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "Producto registrado anteriormente")
    
    def buscar_producto(self, codigo_producto):
    #conexion SQL
        with sqlite3.connect(self.db_name) as conexion: 
            cursor = conexion.cursor()
            sql = "SELECT * FROM Productos WHERE codigo ={}".format(codigo_producto) 
            #ejecución de la consulta sql
            cursor.execute(sql) 
            producto_consulta = cursor.fetchall()
            cursor.close()
    
            return producto_consulta

    def registrar_producto(self):
        if self.validar_formulario() and self.validar_registrar():
            query= 'INSERT INTO Productos VALUES (NULL,?,?,?,?,?,?)'
            #parametros que se obtienen de cada elemento definido en el formulario
            parameters = (self.codigo_producto.get(),self.nombre_producto.get(),self.cantidad.get(),self.categoria.get(), self.desc_producto.get(),self.precio.get())
            #se invonva el metodo para enviarle la consulta y los parastros 
            self.ejecutar_consulta(query, parameters) 
            #se crea una ventana energente informativa para mostrar el mensaje de registro exitoso
            messagebox.showinfo("REGISTRO EXITOSO", f'Se ha registrado correctamente el producto {self.nombre_producto.get()}')
            #se invoca el metodo limpiar formulario para que el formulario nuevamente quede vacio
            self.limpiar_formulario()   
            self.listar_productos()     
        #se creo el metodo para validar que el formulario no tenga campos vacios
    
    def ejecutar_consulta (self, query, parameters=()):
        #conexion a la bd   
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            result = cursor.execute(query, parameters)
            conexion.commit()
        #se retorna el resultado de la ejecución de la sentencia SQL
        return result
    
    def eliminar_producto(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            messagebox.showerror("ERROR", "Debe seleccionar un producto de la tabla")
        query = "DELETE FROM Productos WHERE codigo = ?"
        dato = self.tree.item(self.tree.selection())['text']
        nombre = self.tree.item(self.tree.selection())['values'][0]
        respuesta = messagebox.askquestion("ADVERTENCIA", f"¿Está seguro que desea eliminar el producto: {nombre}?")
        if respuesta == 'yes':
            self.ejecutar_consulta(query, (dato,))
            self.listar_productos()
            messagebox.showinfo('ÉXITO', f'Producto eliminado: {nombre}')
        else:
            messagebox.showerror('ERROR', f'Error al eliminar el producto: {nombre}')
    
    def editar_producto(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            messagebox.showerror("ERROR", "Debe seleccionar un producto de la tabla")
        codigo = self.tree.item(self.tree.selection())['text']
        nombre = self.tree.item(self.tree.selection())['values'][0]
        categoria = self.tree.item(self.tree.selection())['values'][1]
        cantidad = self.tree.item(self.tree.selection())['values'][2]
        precio = self.tree.item(self.tree.selection())['values'][3]
        descripcion = self.tree.item(self.tree.selection())['values'][4]

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("EDITAR PRODUCTO")
        #incluir un icono a la ventana
        self.ventana_editar.iconbitmap("Icon.ico")
        #modificar o no las dimensiones de la ventana
        self.ventana_editar.resizable(0,0)

        label_codigo = Label(self.ventana_editar, text="Código del producto:", font=("Comic Sans", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=8)
        nuevo_codigo = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=codigo), width=25)
        nuevo_codigo.grid(row=0, column=1, padx=5, pady=8)

        label_categoria = Label(self.ventana_editar, text="Categoria:", font=("Comic Sans", 10, "bold")).grid(row=0, column=2, sticky='s', padx=5, pady=8)
        nuevo_combo_categoria = ttk.Combobox(self.ventana_editar, values=["Teclado", "Computador", "Monitor", "Mouse"], width=22, state="readonly")
        nuevo_combo_categoria.set(categoria)
        nuevo_combo_categoria.grid(row=0, column=3, padx=5, pady=0)

        label_nombre = Label(self.ventana_editar, text="Nombre del Producto:", font=("Comic Sans", 10, "bold")).grid(row=1, column=0, sticky='s', padx=5, pady=8)
        nuevo_nombre = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=nombre), width=25)
        nuevo_nombre.grid(row=1, column=1, padx=5, pady=0)

        label_descripcion = Label(self.ventana_editar, text="Descripción:", font=("Comic Sans", 10, "bold")).grid(row=1, column=2, sticky='s', padx=5, pady=8)
        nueva_descripcion = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=descripcion), width=25)
        nueva_descripcion.grid(row=1, column=3, padx=5, pady=0)

        label_cantidad = Label(self.ventana_editar, text="Cantidad:", font=("Comic Sans", 10, "bold")).grid(row=2, column=0, sticky='s', padx=5, pady=8)
        nueva_cantidad = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=cantidad), width=25)
        nueva_cantidad.grid(row=2, column=1, padx=5, pady=0)

        label_precio = Label(self.ventana_editar, text="Precio:", font=("Comic Sans", 10, "bold")).grid(row=2, column=2, sticky='s', padx=5, pady=8)
        nuevo_precio = Entry(self.ventana_editar, textvariable=StringVar(self.ventana_editar, value=nombre), width=25)
        nuevo_precio.grid(row=2, column=3, padx=5, pady=0)

        boton_actualizar = Button(self.ventana_editar, text="ACTUALIZAR", command=lambda:self.actualizar(nuevo_codigo.get(), nuevo_nombre.get(), nueva_cantidad.get(),nuevo_combo_categoria.get(), nuevo_precio.get(), nueva_descripcion.get(), codigo), height=2, width=20, bg="blue", fg="white", font=("Comic Sans MS", 9, "bold"))
        boton_actualizar.grid(row=3, column=1, columnspan=2, padx=10, pady=15)

        self.ventana_editar.mainloop()
    
    def widgets_crud(self):

        #cada que se inicie el sistema se carga el CRUD

        self.label_titulo_crud.config(bd=0) 
        self.label_titulo_crud.grid(row=0, column=0,padx=5,pady=5)
        
        self.titulo_crud = Label (self.label_titulo_crud, text="LISTA DE PRODUCTOS", fg="black", font=("Comic Sans MS", 17, "bold"), pady=10)
        self.titulo_crud.grid(row=0, column=0)

        self.frame_logos_productos.config(bd=0)
        self.frame_logos_productos.grid(row=1, column=0, padx=5, pady=5)

        '''------------ logos de la ventana ------------'''
        #Cargamos la imagen
        imagenes_productos = Image.open('imgs/monitor.png')
        #Tamaño de la imagen
        nueva_imagen = imagenes_productos.resize((40,40))
        #renderizamos las caracteristicas de la imagen
        render = ImageTk.PhotoImage(nueva_imagen)
        #label para cargar la imagen
        label_imagen = Label(self.frame_logos_productos, image=render)
        #renderizo el label
        label_imagen.image = render
        #empaqueto y ubicamos
        label_imagen.grid(row=0,column=0, padx=15, pady=5)
        
        #Cargamos la imagen
        imagenes_productos = Image.open("imgs/computador.png")
        #Tamaño de la imagen
        nueva_imagen = imagenes_productos.resize((40,40))
        #renderizamos las caracteristicas de la imagen
        render = ImageTk.PhotoImage(nueva_imagen)
        #label para cargar la imagen
        label_imagen = Label(self.frame_logos_productos, image=render)
        #renderizo el label
        label_imagen.image = render
        #empaqueto y ubicamos
        label_imagen.grid(row=0,column=1, padx=15, pady=5)
        
        #Cargamos la imagen
        imagenes_productos = Image.open("imgs/mouse.png")
        #Tamaño de la imagen
        nueva_imagen = imagenes_productos.resize((40,40))
        #renderizamos las caracteristicas de la imagen
        render = ImageTk.PhotoImage(nueva_imagen)
        #label para cargar la imagen
        label_imagen = Label(self.frame_logos_productos, image=render)
        #renderizo el label
        label_imagen.image = render
        #empaqueto y ubicamos
        label_imagen.grid(row=0,column=2, padx=15, pady=5)
        
        #Cargamos la imagen
        imagenes_productos = Image.open("imgs/teclado.png")
        #Tamaño de la imagen
        nueva_imagen = imagenes_productos.resize((40,40))
        #renderizamos las caracteristicas de la imagen
        render = ImageTk.PhotoImage(nueva_imagen)
        #label para cargar la imagen
        label_imagen = Label(self.frame_logos_productos, image=render)
        #renderizo el label
        label_imagen.image = render
        #empaqueto y ubicamos
        label_imagen.grid(row=0,column=3, padx=15, pady=5)
        
        '''------------ Marco de la ventana ------------'''
        self.frame_registro.config(bd=2)
        self.frame_registro.grid(row=2,column=0,padx=5,pady=5)
        
        '''------------ Formulario de la ventana ------------'''
        label_codigo_producto = Label(self.frame_registro,text="Codigo del Producto: ", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0, sticky='s', padx=5, pady=10)
        self.codigo_producto = Entry(self.frame_registro, width=25)
        self.codigo_producto.focus()
        self.codigo_producto.grid(row=0, column=1, padx=5, pady=10)
        
        label_nombre_producto = Label(self.frame_registro,text="Nombre del Producto: ", font=("Comic Sans MS", 10, "bold")).grid(row=1, column=0, sticky='s', padx=5, pady=10)
        self.nombre_producto = Entry(self.frame_registro, width=25)
        self.nombre_producto.grid(row=1, column=1, padx=5, pady=10)
        
        label_cantidad = Label(self.frame_registro,text="Cantidad: ", font=("Comic Sans MS", 10, "bold")).grid(row=2, column=0, sticky='s', padx=5, pady=10)
        #cajon para ingresar texto
        self.cantidad = Entry(self.frame_registro, width=25)
        self.cantidad.grid(row=2, column=1, padx=5, pady=10)
        
        label_categoria_producto = Label(self.frame_registro,text="Categoria del Producto: ", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=2, sticky='s', padx=5, pady=10)
        self.categoria = ttk.Combobox(self.frame_registro, values=["Teclado", "Computador", "Monitor", "Mouse"], width=22, state="readonly")
        self.categoria.current(0)
        self.categoria.grid(row=0, column=3, padx=10, pady=10)
        
        label_descripcion_producto= Label(self.frame_registro,text="Descripcion del Producto: ", font=("Comic Sans MS", 10, "bold")).grid(row=1, column=2, sticky='s', padx=5, pady=10)
        self.desc_producto= Entry(self.frame_registro,show="")
        self.desc_producto.grid(row=1,column=3,padx=10,pady=10)
        
        label_precio = Label(self.frame_registro,text="Precio: ", font=("Comic Sans MS", 10, "bold")).grid(row=2, column=2, sticky='s', padx=5, pady=10)
        self.precio = Entry(self.frame_registro, width=25)
        self.precio.grid(row=2, column=3, padx=5, pady=10)
        
        '''------------ Frame de Botones de la ventana ------------'''
        self.frame_botones_registro.config(bd=0)
        self.frame_botones_registro.grid(row=3, column=0, padx=5, pady=5)
        
        '''------------ Botones de la ventana ------------'''
        boton_registrar = Button(self.frame_botones_registro, text="REGISTRAR",command=self.registrar_producto, height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=0, padx=10, pady=15)
        boton_editar = Button(self.frame_botones_registro, text="EDITAR", command=self.editar_producto, height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_eliminar = Button(self.frame_botones_registro, text="ELIMINAR",command=self.eliminar_producto,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        boton_salir = Button(self.frame_botones_registro, text="SALIR",command=self.cerrarVentana,height=2, width=12, bg="green", fg="white", font=("Comic Sans MS", 10,"bold")).grid(row=0, column=3, padx=10, pady=15)

        '''------------ Tabla con la lista de Productos ------------'''
        self.frame_tabla_crud.config(bd=2)
        self.frame_tabla_crud.grid(row=4, column=0, padx=5, pady=5)
        self.tree = ttk.Treeview(self.frame_tabla_crud, height=13, columns=("columna1", "columna2", "columna3", "columna4", "columna5"))
        self.tree.heading("columna1", text='Nombre', anchor=CENTER)
        self.tree.column("columna1", width=150, minwidth=75, stretch=False)
        
        self.tree.heading("columna2", text='Categoria', anchor=CENTER)
        self.tree.column("columna2", width=150, minwidth=75, stretch=False)
        
        self.tree.heading("columna3", text='Cantidad', anchor=CENTER)
        self.tree.column("columna3", width=150, minwidth=75, stretch=False)
        
        self.tree.heading("columna4", text='Precio', anchor=CENTER)
        self.tree.column("columna4", width=150, minwidth=75, stretch=False)
        
        self.tree.heading("columna5", text='Descripcion', anchor=CENTER)
        self.tree.column("columna5", width=150, minwidth=75, stretch=False)
        
        self.tree.grid(row=0, column=0, sticky=E)
        self.listar_productos()
        self.widgets_buscador_remove()
        self.label_informacion.grid_remove()
        
    def widgets_buscador(self):
        self.label_titulo_buscador.config(bd=0)
        self.label_titulo_buscador.grid(row=0, column=0, padx=5, pady=5)

        # Título
        self.titulo_buscador = Label(self.label_titulo_buscador, text="BUSCADOR DE PRODUCTOS", fg="black", font=("Comic Sans", 17, "bold"))
        self.titulo_buscador.grid(row=0, column=0)

        # Frame buscar
        self.frame_buscar_producto.config(bd=2)
        self.frame_buscar_producto.grid(row=2, column=0, padx=5, pady=5)

        # Formulario Buscar
        self.label_buscar = Label(self.frame_buscar_producto, text="Buscar Por: ", font=("Comic Sans", 18, "bold")).grid(row = 0 , column=0, sticky="s", padx=5, pady=5)
        self.combo_buscar = ttk.Combobox(self.frame_buscar_producto, values=["codigo", "nombre"], width=22, state="readonly")
        self.combo_buscar.current(0)
        self.combo_buscar.grid(row=0, column=1, padx=5, pady=5)
        
        # Label codigo_nombre
        self.label_codigo_nombre = Label(self.frame_buscar_producto, text="Codigo / Nombre del producto: ", font=("Comic Sans", 10, "bold"))
        self.label_codigo_nombre.grid(row=0, column=2, sticky='s', padx=5, pady=5)
        self.codigo_nombre = Entry(self.frame_buscar_producto, width=25)
        self.codigo_nombre.focus()
        self.codigo_nombre.grid(row=0, column=3, padx=10, pady=5)

        # Frame marco
        self.frame_boton_buscar.config(bd=0)
        self.frame_boton_buscar.grid(row=3, column=0, padx=5, pady=5)

        # Boton
        self.boton_buscar = Button(self.frame_boton_buscar, text="BUSCAR", command=self.buscar_productos, height=2, width=28, bg="black", fg="white", font=("Comic Sans", 18, "bold"))
        self.boton_buscar.grid(row=0, column=0, padx=5, pady=5)

        # Se carga la tabla pero sin datos
        self.tree.delete(*self.tree.get_children())

        # Remover otros widgets de otros formularios
        self.widgets_crud_remove()
        self.label_informacion.grid_remove()
        
    def widgets_crud_remove(self):
        # Remove permite que al cambiar de una ventana a otra se limpie (cargue la nueva ventana solicitada, pasara de registro a buscar o viceversa)
        # Se limpia label y se carga los nuevos
        self.label_titulo_crud.grid_remove()
        self.frame_registro.grid_remove()
        self.frame_botones_registro.grid_remove()

    def widgets_buscador_remove(self):
        self.label_titulo_buscador.grid_remove()
        self.frame_buscar_producto.grid_remove()
        self.frame_boton_buscar.grid_remove()

    def widgets_informacion(self):
        # Se ocultan los frame de los logos y de la tabla para que no carguen en Ayuda
        self.frame_logos_productos.grid_forget()
        self.frame_tabla_crud.grid_forget()

        self.label_informacion.config(bd=0)
        self.label_informacion.grid(row=0, column=0)

        # Título
        self.label_titulo = Label(self.label_informacion, text="APLICACIÓN DE ESCRITORIO", fg="white", bg="black", font=("Comic Sans", 25, "bold"), padx=137, pady=20)
        self.label_titulo.grid(row=0, column=0)

        # Logos imágenes
        # Logo
        imagen_soporte = Image.open("imgs/info.png")
        nueva_imagen = imagen_soporte.resize((100, 100))
        render = ImageTk.PhotoImage(nueva_imagen)
        label_imagen = Label(self.label_informacion, image=render)
        label_imagen.image = render
        label_imagen.grid(row=1, column=0, padx=10, pady=15)

        # Opciones
        self.label_titulo = Label(self.label_informacion, text="> Código de Tienda de Tecnología", fg="black", font=("Comic Sans", 18, "bold"))
        self.label_titulo.grid(row=2, column=0, sticky=W, padx=30, pady=10)

        self.label_titulo = Label(self.label_informacion, text="> En esta tienda encuentra productos de Tecnología", fg="black", font=("Comic Sans", 18, "bold"))
        self.label_titulo.grid(row=3, column=0, sticky=W, padx=30, pady=10)

        self.label_titulo = Label(self.label_informacion, text="> Instructor Yuly Sáenz", fg="black", font=("Comic Sans", 18, "bold"))
        self.label_titulo.grid(row=4, column=0, sticky=W, padx=30, pady=10)

        self.label_titulo = Label(self.label_informacion, text="Creado por Yuly Sáenz Ficha 2560152 Tgo. ADSO 2023", fg="black", font=("Comic Sans", 10, "bold"))
        self.label_titulo.grid(row=6, column=0, pady=60)

        # Remove de las otras ventanas para cargar la nueva
        self.widgets_buscador_remove()
        self.widgets_crud_remove()

    def widgets_clientes(self):
        pass

    def buscar_productos (self):

        if(self.validar_busqueda()): #Obtener todos los elementos con get_children(), que retorna una tupla. 
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)

        #se puede realizar la busqueda en el formulario por codigo

        #combo_buscar es el combo que tiene los campos por los cuales se puede realizar la busqueda

        if (self.combo_buscar.get()== 'codigo'): #sentencia SQL LIKE-> inicie por una letra o varias o completas
            query=("SELECT * FROM Productos WHERE codigo LIKE?")
            #% permite realizar la busqueda sin tener completa del codigo a buscar (busqueda parcial de la palabra y luego clic en buscar)
            parameters=(self.codigo_nombre.get()+"%")
            #enviamos a ejecutar_consulta (conexion a la bd para realizar la query) el query y los parametros 
            db_rows = self.ejecutar_consulta(query, (parameters,))
            #db_rows es una lista
            for row in db_rows:
            #se inserta las conincidencias de busqueda en la tabla por cada parametro de busqueda
                self.tree.insert("",0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6])) 
            #busqueda vacia (cuando el producto no esta almacenado en la bd)
            #el get children lo volvemos una lista o varias o completas en la tabla
            if(list(self.tree.get_children())==[]):
               messagebox.showerror("ERROR", "Producto no encontrado")
        #muestra ventana
        else:
        #sentencia SQL LIKE > inicie por
            query=("SELECT * FROM Productos WHERE nombre LIKE ?")
            #% permite realizar la busqueda sin tener completa del nombre a buscar (busqueda parcial de la palabra y luego clic en buscar)
            parameters = ("%"+self.codigo_nombre.get()+"*")
            #enviamos a ejecutar consulta (conexion a la bd para realizar la query) el query y los parametros
            db_rows = self.ejecutar_consulta(query, (parameters,))
            #db rows es una lista
            for row in db_rows:
                #se inserta las conincidencias de busqueda en la tabla por cada parametro de busqueda
                self.tree.insert("",0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))
            #busqueda vacia (cuando el producto no esta almacenado en la bd)
            #al get children lo volvemos una lista o varias o completas en la tabla

            if(list(self.tree.get_children())==[]): 
                #muestra ventana
                messagebox.showmerror("ERROR","Producto no encontrado")             
                
    def actualizar(self,nuevo_codigo, nuevo_nombre,nuevo_combo_categoria,nueva_cantidad,nuevo_precio,nueva_descripcion,codigo):
        query ='UPDATE Productos SET codigo= ?, nombre= ?, categoria= ?, cantidad = ?, precio= ?, descripcion = ? WHERE codigo = ?'
        parameters = (nuevo_codigo, nuevo_nombre, nuevo_combo_categoria, nueva_cantidad, nuevo_precio, nueva_descripcion, codigo)
        self.ejecutar_consulta(query, parameters)
        messagebox.showinfo('EXITO', f'Producto Actualizado:{nuevo_nombre}')
        self.ventana_editar.destroy()
        self.listar_productos()
    
    def validar_busqueda(self):
        if len(self.codigo_nombre.get()) != 0:
            return True
        else:
            self.tree.delete(*self.tree.get_children())
            messagebox.showerror("ERROR", "Complete todos los campos para la busqueda")
    
    def validar_registrar(self):
        parameters = self.codigo_producto.get()
        query= "SELECT * FROM Productos WHERE codigo = ?"
        dato = self.ejecutar_consulta(query,(parameters,))
        if (dato.fetchall()==[]):
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "Codigo registrado anteriormente")
        
    def cerrarVentana(self):
        ventana_productos.destroy()
    
    def limpiar_formulario(self):
        self.codigo_producto.delete(0, END)
        self.nombre_producto.delete(0, END)
        self.cantidad.delete(0, END)
        self.categoria.delete(0, END)
        self.desc_producto.delete(0, END)
        self.precio.delete(0, END)
        
    def listar_productos(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        query = 'SELECT * FROM Productos ORDER BY nombre DESC'
        db_rows = self.ejecutar_consulta(query)
        for row in db_rows:
            self.tree.insert("",0, text=row[1], values=(row[2], row[3], row[4], row[5], row[6]))
            
    def limpiar_tabla(self):
        self.tree.delete(*self.tree.get_children())
    
if __name__=='__main__':
    ventana_productos = Tk()
    application = Productos(ventana_productos)
    ventana_productos.mainloop()  