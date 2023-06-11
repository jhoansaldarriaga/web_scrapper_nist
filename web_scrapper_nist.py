import tkinter as tk
import requests
from bs4 import BeautifulSoup
import csv

# Variables globales para almacenar los resultados del scraping
encabezados = []
datos_tablas = []

# Función para extraer y mostrar la tabla en la interfaz gráfica
def mostrar_tabla():
    direccion = entrada_enlace.get()  # Obtener el enlace ingresado
    resultado = scrapper(direccion)  # Obtener los datos de la tabla
    
    if resultado:
        global encabezados, datos_tablas
        encabezados, datos_tablas = resultado
        
        if len(datos_tablas) >= 2:
            etiqueta_estado.config(text="Hay " + str(len(datos_tablas)) + " tablas. Seleccione el número de tabla:")
            boton_generar.config(state=tk.DISABLED)  # Deshabilitar el botón mientras se selecciona la tabla
            entrada_num_tabla.config(state=tk.NORMAL)  # Habilitar el campo de entrada para el número de tabla
            entrada_num_tabla.delete(0, tk.END)  # Limpiar el campo de entrada
        else:
            mostrar_tabla_seleccionada(0)  # Mostrar la única tabla disponible
    else:
        etiqueta_estado.config(text="No se pudo obtener la tabla")

def mostrar_tabla_seleccionada(num_tabla):
    # Mostrar el encabezado
    tabla_text.delete("1.0", tk.END)  # Limpiar el widget de texto
    tabla_text.insert(tk.END, "\t".join(encabezados[num_tabla]) + "\n")
    # Mostrar los datos de la tabla seleccionada
    for fila in datos_tablas[num_tabla]:
        tabla_text.insert(tk.END, "\t".join(fila) + "\n")
    etiqueta_estado.config(text="Tabla generada exitosamente")
    
    nombre_archivo = entrada_archivo.get()
    crear_archivo(encabezados[num_tabla], datos_tablas[num_tabla], nombre_archivo)

def crear_archivo(encabezado, datos, nombre_archivo):
    with open(nombre_archivo, "w", newline="") as archivo:
        escribircsv = csv.writer(archivo)
        escribircsv.writerow(encabezado)
        escribircsv.writerows(datos)

#SCRAPPER PARA TABLAS
def scrapper(direccion):
    try:
        #INVOCACION DE LOS DATOS DE UNA PAGINA WEB
        pagina_web = requests.get(direccion)  #descargar pagina
        soup = BeautifulSoup(pagina_web.content, "html.parser") #creando objeto tipo SOUP completo

        #extraer tabla
        tabla = soup.find_all("table", class_="small") #find un elemento y #find_all una lista de elementos
        if len(tabla) >= 2:
            # Se extraen los encabezados y los datos de cada tabla
            encabezados = []
            datos_tablas = []
            for t in tabla:
                fila = t.find_all("tr")
                encabezado = fila[0].find_all("th")
                encabezados.append([e.text for e in encabezado])

                datos = []
                for indice in range(1, len(fila)):
                    valores = fila[indice].find_all("td", align="right")
                    objetos = [v.text for v in valores]
                    datos.append(objetos)

                datos_tablas.append(datos)
            
            return encabezados, datos_tablas
        elif len(tabla) == 1:
            # Si solo hay una tabla, se extraen los encabezados y los datos
            fila = tabla[0].find_all("tr")
            encabezado = fila[0].find_all("th")
            encabezados = [e.text for e in encabezado]

            datos = []
            for indice in range(1, len(fila)):
                valores = fila[indice].find_all("td", align="right")
                objetos = [v.text for v in valores]
                datos.append(objetos)

            return [encabezados], [datos]
        else:
            return None

    except:
        return None

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Archivos")
ventana.geometry("800x600")

# Crear una etiqueta y un campo de entrada para el enlace
etiqueta_enlace = tk.Label(ventana, text="Enlace:")
etiqueta_enlace.pack()
entrada_enlace = tk.Entry(ventana, width=50)
entrada_enlace.pack()

etiqueta_archivo = tk.Label(ventana, text="Nombre del archivo CSV:")
etiqueta_archivo.pack()
entrada_archivo = tk.Entry(ventana, width=50)
entrada_archivo.pack()

# Crear un botón para generar el archivo
boton_generar = tk.Button(ventana, text="Generar Tabla", command=mostrar_tabla)
boton_generar.pack()

# Crear una etiqueta para mostrar el estado de generación de la tabla
etiqueta_estado = tk.Label(ventana, text="")
etiqueta_estado.pack()

# Crear un campo de entrada para el número de tabla
etiqueta_num_tabla = tk.Label(ventana, text="Número de tabla:")
etiqueta_num_tabla.pack()
entrada_num_tabla = tk.Entry(ventana, width=50, state=tk.DISABLED)  # Campo de entrada deshabilitado inicialmente
entrada_num_tabla.pack()

# Crear un botón para seleccionar la tabla
boton_seleccionar_tabla = tk.Button(ventana, text="Seleccionar Tabla", command=lambda: mostrar_tabla_seleccionada(int(entrada_num_tabla.get()) - 1))
boton_seleccionar_tabla.pack()

# Crear un widget Text para mostrar la tabla
tabla_text = tk.Text(ventana)
tabla_text.pack()

# Iniciar el bucle de eventos de la interfaz gráfica
ventana.mainloop()