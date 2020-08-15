import os
import traffic
from traffic.core import Traffic
import pandas as pd


def guardarcsv(archivo, nombre_archivo,carpeta_datos_csv = "datos_sectores" ):
    # esta funciona genera una carpeta sino existe, y guarda los datos descargados en esta
    if not os.path.exists(carpeta_datos_csv):
        os.mkdir(carpeta_datos_csv)
    # guarda el archivo .csv en la carpeta especificada
    carpeta_datos_csv = r"datos_sectores/"
    archivo.to_csv(carpeta_datos_csv+nombre_archivo+".csv")

def cargardatos(carpeta,nombre_datos):
    # carga los datos descargados desde una carpeta
    datos_cargados = Traffic.from_file(carpeta+nombre_datos)
    return datos_cargados

def cargardatosfiltrados(carpeta,nombre_datos):
    # carga los datos descargados desde una carpeta y pone formato de tiempos
    
    
    datos_cargados = Traffic.from_file(carpeta+nombre_datos)
    Var_time = ["hour", "last_position", "timestamp"]
    datos_cargados.data[Var_time] = datos_cargados.data[Var_time] = datos_cargados.data[Var_time].astype("datetime64[ns, UTC]")
    datos_cargados.data = datos_cargados.data.drop(["Unnamed: 0.1","Unnamed: 0","alert","geoaltitude",'hour','last_position','onground','spi','squawk','vertical_rate'],axis = 1)
    return datos_cargados

    