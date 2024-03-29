import traffic
from traffic.core import Traffic
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime


def guardarimagen(carpeta_imagenes,nombre_figura):
     # esta funcion guarda las imágenes por directorios, el principal es      
     # imagenes_libros/carpeta_imágenes/nombre_figura.png
    if not os.path.exists("imagenes_libros"):
        os.mkdir("imagenes_libros")
    if not os.path.exists("imagenes_libros/"+carpeta_imagenes):
        os.mkdir("imagenes_libros/"+carpeta_imagenes)
    plt.savefig(fname = "imagenes_libros/" + carpeta_imagenes+"/"+nombre_figura,dpi = 300)
    
def guardarcsv(archivo, nombre_archivo,carpeta_datos_csv = "datos_sectores/" ):
    # esta funciona genera una carpeta sino existe, y guarda los datos descargados en esta
    if not os.path.exists(carpeta_datos_csv):
        os.mkdir(carpeta_datos_csv)
    # guarda el archivo .csv en la carpeta especificada
    carpeta_datos_csv = r"datos_sectores/"
    archivo.to_csv(carpeta_datos_csv+nombre_archivo+".csv")

def cargardatos(carpeta,nombre_datos):
    # carga datos descargos desde carpeta, y cambia variables de tiempo a UTC
    Var_time = ["hour", "last_position", "timestamp"]
    datos_cargados = Traffic.from_file(carpeta+nombre_datos)
    #datos_cargados.data = datos_cargados.data.drop(['Unnamed: 0'])
    datos_cargados.data[Var_time] = datos_cargados.data[Var_time] = datos_cargados.data[Var_time].astype("datetime64[ns, UTC]")
    return datos_cargados

"""
def cargardatosfiltrados(carpeta,nombre_datos):
    # carga los datos descargados desde una carpeta y pone formato de tiempos
    datos_cargados = Traffic.from_file(carpeta+nombre_datos)
    Var_time = ["hour", "last_position", "timestamp"]
    datos_cargados.data[Var_time] = datos_cargados.data[Var_time] = datos_cargados.data[Var_time].astype("datetime64[ns, UTC]")
    datos_cargados.data = datos_cargados.data.drop(["Unnamed: 0.1","Unnamed: 0","alert","geoaltitude",'hour','last_position','onground','spi','squawk','vertical_rate'],axis = 1)
    return datos_cargados
"""

def origenmismoinstante(datos):
    # pone los datos con el mismo origen independientemente del día
    datos = Traffic(datos)
    timestamp = pd.Series([])
    listado_aves = datos.data.flight_id.unique()
    for ave in listado_aves:
    # Seleccionamos la trayectoria de la aeronave y creamos una copia 
        tray = datos[ave].data
        tray2 = tray
        
        # Seleccionamos el instante de tiempo inicial
        init_time = tray.timestamp.iloc[0]
        # El instante inicial lo restamos, hay que tener cuidado con que no se convierta en timedelta ya que el formato es datetime
        # añadida parte para poder poner datos de varios días
        tray2_timestamp = tray.timestamp - datetime.timedelta(days = init_time.day, hours = init_time.hour, minutes = init_time.minute, seconds = init_time.second)
        #Los nuevos timestamp los metemos en una columna que más tarde la cambiaremos para que coincida con todos los vuelos de la BBDD
        timestamp = timestamp.append(tray2_timestamp)
    datos.data.timestamp = timestamp
    return datos