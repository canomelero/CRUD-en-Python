import tkinter as tk

from pedidos_clase import Pedidos
from tkinter import ttk

#############################################################################################################
# Variables
pedidos = Pedidos()

# Tk() -> Clase que crea la ventana principal de la app
app = tk.Tk()  
opcion = tk.IntVar()
segundaOpcion = tk.IntVar()
imagen_fondo = tk.PhotoImage(file="./PantallaInicio.png") 

# Creación de los frames para cada opción y menú
pantallaInicial = tk.Frame(app, bg = "lightblue")   
menuPrincipal = tk.Frame(app, bg = "lightcoral")
segundoMenu = tk.Frame(app, bg = "lightgreen")
pantallaOpc1 = tk.Frame(app, bg = "lightgreen")
pantallaOpc3 = tk.Frame(app, bg = "blue")
frameTablaStock = tk.Frame(app)
frameTablaPedido = tk.Frame(app)
frameTablaDetPed = tk.Frame(app)
frameDatosPedido = tk.Frame(app, bg="lightgreen")

# Añadir la imagen de fondo de la pantalla principal
label_fondo = tk.Label(pantallaInicial, image=imagen_fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)


#############################################################################################################
def mostrarPantalla(frame):
    # pack_forget() -> Método de la clase Frame para ocutlar un widget que ha sido posicionado en la interfaz
    pantallaInicial.pack_forget()
    menuPrincipal.pack_forget()
    pantallaOpc1.pack_forget()
    pantallaOpc3.pack_forget()
    frameTablaStock.pack_forget()
    frameTablaPedido.pack_forget()
    frameTablaDetPed.pack_forget()
    frameDatosPedido.pack_forget()

    # pack() -> Método de la clase Frame que muestra un widget en la pantalla
    frame.pack(fill = 'both', expand = True) 


def limpiarFrame(frame):
    # Elimina todos los widgets hijos de un Frame
    for widget in frame.winfo_children():
        widget.destroy()

def creacionBorradoTablas(archivo):
    pedidos.crear_tablas(archivo.get()) 
    mostrarPantalla(menuPrincipal)


def accionPrincipal1():
    mostrarPantalla(pantallaOpc1)

    # Creación del Frame que contendrá la información
    frameAux = tk.Frame(pantallaOpc1, bg = "lightgreen")
    frameAux.pack(expand = True)

    mensaje = tk.Label(frameAux, text = "Indique el nombre archivo .sql desde \nla ruta actual (ponga 'nombre_archivo.sql')",
                       bg = "lightgreen", font=("Arial", 16))
    mensaje.pack()

    respuesta = tk.Entry(frameAux, width = 30)
    respuesta.pack(pady = 20)

    pedidos.cursor.execute("SAVEPOINT s1;")

    btnConfirmar = tk.Button(
        frameAux, 
        text = "Confirmar",
        width = 7,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 12),
        command = lambda : creacionBorradoTablas(respuesta)
    )

    # Ubicación de botón en el centro de la pantalla
    btnConfirmar.pack(pady = 10)


def cargarTablaStock():
    mostrarPantalla(frameTablaStock)
    
    pedidos.cursor.execute(f"SELECT * FROM stock LIMIT 0")
    columns = [description[0] for description in pedidos.cursor.description]

    tablaStock = pedidos.obtener_stock()

    # Limpiar los frames hijos creados anteriormente
    limpiarFrame(frameTablaStock)
    
    # Crear un sub-frame específico para la tabla
    frameTablaAux = tk.Frame(frameTablaStock)
    frameTablaAux.pack(expand = True, fill = "both")

    tree = ttk.Treeview(frameTablaAux, columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for row in tablaStock:
        tree.insert("", "end", values=row)

    frameTablaAux.grid_rowconfigure(0, weight = 1)
    frameTablaAux.grid_columnconfigure(0, weight = 1)

    btnVolver = tk.Button(
        frameTablaStock, 
        text = "Volver",
        width = 7,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 12),
        command = lambda : mostrarPantalla(pantallaOpc3)    
    )

    btnVolver.pack(pady = 10)

def cargarTablaPedio():
    mostrarPantalla(frameTablaPedido)
    
    pedidos.cursor.execute(f"SELECT * FROM pedido LIMIT 0")
    columns = [description[0] for description in pedidos.cursor.description]

    tablaPedido = pedidos.obtener_pedido()

    # Limpiar los frames hijos creados anteriormente
    limpiarFrame(frameTablaPedido)

    # Crear un sub-frame específico para la tabla
    frameTablaAux = tk.Frame(frameTablaPedido)
    frameTablaAux.pack(expand = True, fill = "both")

    tree = ttk.Treeview(frameTablaAux, columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for row in tablaPedido:
        tree.insert("", "end", values=row)

    frameTablaAux.grid_rowconfigure(0, weight = 1)
    frameTablaAux.grid_columnconfigure(0, weight = 1)

    btnConfirmar = tk.Button(
        frameTablaPedido, 
        text = "Volver",
        width = 7,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 12),
        command = lambda : mostrarPantalla(pantallaOpc3)      
    )

    btnConfirmar.pack(pady = 20)


def cargarTablaDetallePed():
    mostrarPantalla(frameTablaDetPed)
    
    pedidos.cursor.execute(f"SELECT * FROM detalle_pedido LIMIT 0")
    columns = [description[0] for description in pedidos.cursor.description]

    tablaDetallePed = pedidos.obtener_detalle_pedido()

    # Limpiar los frames hijos creados anteriormente
    limpiarFrame(frameTablaDetPed)

    # Crear un sub-frame específico para la tabla
    frameTablaAux = tk.Frame(frameTablaDetPed)
    frameTablaAux.pack(expand = True, fill = "both")

    tree = ttk.Treeview(frameTablaAux, columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for row in tablaDetallePed:
        tree.insert("", "end", values=row)

    frameTablaAux.grid_rowconfigure(0, weight = 1)
    frameTablaAux.grid_columnconfigure(0, weight = 1)

    btnConfirmar = tk.Button(
        frameTablaDetPed, 
        text = "Volver",
        width = 7,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 12),
        command = lambda : mostrarPantalla(pantallaOpc3)    
    )

    btnConfirmar.pack(pady = 20)

def cargarTabla(opcion):
    if opcion.get() == 1:
        cargarTablaPedio()
    elif opcion.get() == 2:
        cargarTablaStock()
    else :
        cargarTablaDetallePed()
    

def accionPrincipal3():
    mostrarPantalla(pantallaOpc3)

    # Limpiar los frames hijos creados anteriormente
    limpiarFrame(pantallaOpc3)

    # Crear un sub-Frame para centrar los Radiobuttons usando grid
    frameOpcion = tk.Frame(pantallaOpc3, bg = "blue")
    frameOpcion.pack(expand = True)  # Pack dentro del frame_principal

    opcion1 = tk.Radiobutton(frameOpcion, text = "Tabla Pedido", variable = opcion, value = 1, 
                             bg = "blue", highlightthickness = 0, font=("Arial", 16))
    opcion2 = tk.Radiobutton(frameOpcion, text = "Tabla Stock", variable = opcion, value = 2,
                             bg = "blue", highlightthickness = 0, font=("Arial", 16))
    opcion3 = tk.Radiobutton(frameOpcion, text = "Tabla Detalle - Pedido", variable = opcion, 
                             value = 3, bg = "blue", highlightthickness = 0, font=("Arial", 16))

    opcion1.pack(pady = 10)
    opcion2.pack(pady = 10)
    opcion3.pack(pady = 10)

    btnConfirmar = tk.Button(
        frameOpcion, 
        text = "Confirmar",
        width = 7,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 12),
        command = lambda : cargarTabla(opcion)    
    )

    btnConfirmar.pack(pady = 20)

    btnVolver = tk.Button(
        frameOpcion, 
        text = "Volver",
        width = 7,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 12),
        command = lambda : mostrarPantalla(menuPrincipal)    
    )

    btnVolver.pack(pady = 10)

def realizarAccion():
    seleccion = opcion.get()

    if seleccion == 1:
        accionPrincipal1()
    elif seleccion == 2:
        accionDatosPedido()
    elif seleccion == 3:
        accionPrincipal3()
    elif seleccion == 4:
        pedidos.cerrar_conex()
        app.destroy()


def realizarSegundaAccion():
    seleccion = segundaOpcion.get()

    if seleccion == 1:
        pedidos.obtener_cantidad_producto()
    elif seleccion == 2:
        pedidos.eliminar_detalles_pedido()
    elif seleccion == 3:
        pedidos.eliminar_detalles_y_pedido()
    elif seleccion == 4:
        pedidos.connection.commit()
        mostrarPantalla(menuPrincipal)


def cargarMenuPrincipal(frame):
    mostrarPantalla(frame)

    # Crear un sub-Frame para centrar los Radiobuttons usando grid
    frameOpcion = tk.Frame(frame, bg = "lightcoral")
    frameOpcion.pack(expand = True)  # Pack dentro del frame_principal

    opcion1 = tk.Radiobutton(frameOpcion, text = "1. Borrado y creación de tablas con inserción de 10 tuplas ", 
                             variable = opcion, value = 1, bg = "lightcoral", highlightthickness = 0, font=("Arial", 16))
    opcion2 = tk.Radiobutton(frameOpcion, text = "2. Dar de alta nuevo pedido", variable = opcion, value = 2,
                             bg = "lightcoral", highlightthickness = 0, font=("Arial", 16))
    opcion3 = tk.Radiobutton(frameOpcion, text = "3. Mostrar contenido de las tablas de la BD", variable = opcion, 
                             value = 3, bg = "lightcoral", highlightthickness = 0, font=("Arial", 16))
    opcion4 = tk.Radiobutton(frameOpcion, text = "4. Salir del programa y cerrar conexión a la BD", variable = opcion, 
                             value = 4, bg = "lightcoral", highlightthickness = 0, font=("Arial", 16))

    opcion1.pack(pady = 10)
    opcion2.pack(pady = 10)
    opcion3.pack(pady = 10)
    opcion4.pack(pady = 10)

    btnConfirmar = tk.Button(
        frameOpcion, 
        text = "Confirmar",
        width = 10,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 16),
        command = realizarAccion    # la función se pasa como referencia y será llamada cuando el botón se presione 
    )

    # Ubicación de botón en el centro de la pantalla
    btnConfirmar.pack(pady=30)


def cargarSegundoMenu(frame):
    mostrarPantalla(frame)

    # Crear un sub-Frame para centrar los Radiobuttons usando grid
    frameOpcion = tk.Frame(frame, bg = "lightgreen")
    frameOpcion.pack(expand = True)  # Pack dentro del frame_principal

    opcion1 = tk.Radiobutton(frameOpcion, text = "1. Añadir detalle de producto ", 
                             variable = segundaOpcion, value = 1, bg = "lightgreen", highlightthickness = 0, font=("Arial", 16))
    opcion2 = tk.Radiobutton(frameOpcion, text = "2. Eliminar todos los detalles del producto", variable = segundaOpcion, value = 2,
                             bg = "lightgreen", highlightthickness = 0, font=("Arial", 16))
    opcion3 = tk.Radiobutton(frameOpcion, text = "3. Cancelar el pedido", variable = segundaOpcion, 
                             value = 3, bg = "lightgreen", highlightthickness = 0, font=("Arial", 16))
    opcion4 = tk.Radiobutton(frameOpcion, text = "4. Finalizar pedido", variable = segundaOpcion  , 
                             value = 4, bg = "lightgreen", highlightthickness = 0, font=("Arial", 16))

    opcion1.pack(pady = 10)
    opcion2.pack(pady = 10)
    opcion3.pack(pady = 10)
    opcion4.pack(pady = 10)

    btnConfirmar = tk.Button(
        frameOpcion, 
        text = "Confirmar",
        width = 10,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 16),
        command = realizarSegundaAccion    # la función se pasa como referencia y será llamada cuando el botón se presione 
    )

    # Ubicación de botón en el centro de la pantalla
    btnConfirmar.pack(pady=60)


def cargarPantallaInicio(app):
    app.geometry("800x600")  # geometry() -> establecer tamaño de la ventana
    app.title("Seminario 1 - DDSI")

    mostrarPantalla(pantallaInicial)

    # Creación de botón
    # lambda permite que se ejecute la función solo cuando se haga click sobre el botón
    btnIniciar = tk.Button(
        pantallaInicial, 
        text = "Iniciar",
        width = 10,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 16),
        command = lambda : cargarMenuPrincipal(menuPrincipal)
    )

    # Ubicación de botón en el centro de la pantalla
    btnIniciar.place(x=400, y=450, anchor="center")


def accionDatosPedido():
    mostrarPantalla(frameDatosPedido)

    limpiarFrame(frameDatosPedido)

    # Creación del Frame que contendrá la información
    frameAux = tk.Frame(frameDatosPedido, bg = "lightgreen")
    frameAux.pack(expand = True)

    mensaje1 = tk.Label(frameAux, text = "Código de pedido",
                       bg = "lightgreen", font=("Arial", 16))
    mensaje1.pack()

    codigoPedido = tk.Entry(frameAux, width = 30)
    codigoPedido.pack(pady = 20)

    mensaje2 = tk.Label(frameAux, text = "Número de cliente",
                       bg = "lightgreen", font=("Arial", 16))
    mensaje2.pack()

    numeroCliente = tk.Entry(frameAux, width = 30)
    numeroCliente.pack(pady = 20)

    mensaje3 = tk.Label(frameAux, text = "Fecha del pedido",
                       bg = "lightgreen", font=("Arial", 16))
    mensaje3.pack()

    fechaPedido = tk.Entry(frameAux, width = 30)
    fechaPedido.pack(pady = 20)

    btnConfirmar = tk.Button(
        frameAux, 
        text = "Confirmar",
        width = 7,
        height = 3,
        relief = "groove", 
        borderwidth = 2,
        bg = "#CCFF99",
        font=("Arial", 12),
        command = lambda : (pedidos.aniadir_pedido(codigoPedido.get(), int(numeroCliente.get()), fechaPedido.get()), cargarSegundoMenu(segundoMenu))
    )

    # Ubicación de botón en el centro de la pantalla
    btnConfirmar.pack(pady = 10)



#############################################################################################################

if __name__ == "__main__":
    
    cargarPantallaInicio(app)
    
    # mainloop() -> método encargado de ir actualizando la pantalla 
    app.mainloop()     






