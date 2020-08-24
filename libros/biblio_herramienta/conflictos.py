import traffic
from traffic.core import Traffic
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime


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

def crearparejas(BBDD):
    # crea parejas de aviones
    pairs = []
    listado_aves = BBDD.flight_id.unique()
    for ave1 in listado_aves:
        for ave2 in listado_aves:
            if ave1 == ave2:
                pass
            else:
                pairs.append([ave1, ave2])
    pairs = pd.DataFrame(pairs)
    pairs.columns = ["ave1", "ave2"]
    return pairs

def generadorDFconflictos(datos,pares):
    # genera los DF que realizan los conflictos
    if not isinstance(datos,Traffic):
        datos = Traffic(datos)
    Datos_ave1 = datos.data.iloc[0:0]
    Datos_ave2 = datos.data.iloc[0:0]
    for index, row in pares.iterrows():
        # Seleccionamos cada una de las aeronaves que aparecen en las parejas
        tray_ave1 = datos[row['ave1']].data
        tray_ave2 = datos[row['ave2']].data
        #Obtenemos los datos de entrada de cada aeronave
        init_values_ave1 = tray_ave1.iloc[0]
        init_values_ave2 = tray_ave2.iloc[0]
        # Metemos esta información en un DataFrame para cada aeronave
        Datos_ave1 = Datos_ave1.append(init_values_ave1)
        Datos_ave2 = Datos_ave2.append(init_values_ave2)
    return Datos_ave1, Datos_ave2