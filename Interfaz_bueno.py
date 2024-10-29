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
pantallaOpc3 = tk.Frame(app, bg = "black")

# Añadir la imagen de fondo de la pantalla principal
label_fondo = tk.Label(pantallaInicial, image=imagen_fondo)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)


#############################################################################################################
def mostrarPantalla(frame):
    # pack_forget() -> Método de la clase Frame para ocutlar un widget que ha sido posicionado en la interfaz
    pantallaInicial.pack_forget()
    menuPrincipal.pack_forget()
    pantallaOpc3.pack_forget()

    # pack() -> Método de la clase Frame que muestra un widget en la pantalla
    frame.pack(fill = 'both', expand = True) 


def cargarTablasBD():
    mostrarPantalla(pantallaOpc3)
    
    #pedidos.mostrar_tablas("SELECT * FROM ")
    pedidos.cursor.execute(f"SELECT * FROM pedido LIMIT 0")
    columns = [description[0] for description in pedidos.cursor.description]

    tree = ttk.Treeview(pantallaOpc3, columns=columns, show="headings")
    tree.grid(row=0, column=0, sticky="nsew")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    #for row in rows:
    #    tree.insert("", "end", values=row)

    pantallaOpc3.grid_rowconfigure(0, weight = 1)
    pantallaOpc3.grid_columnconfigure(0, weight = 1)


def realizarAccion():
    seleccion = opcion.get()

    if seleccion == 1:
        print("Opcion 1")
    elif seleccion == 2:
        pedidos.aniadir_pedido()
        cargarSegundoMenu(segundoMenu)
    elif seleccion == 3:
        cargarTablasBD()
    elif seleccion == 4:
        print("Cerrando conexión...")
        pedidos.cerrar_conex()


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



#############################################################################################################

if __name__ == "__main__":
    
    cargarPantallaInicio(app)
    
    # mainloop() -> método encargado de ir actualizando la pantalla 
    app.mainloop()     




