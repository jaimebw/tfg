import traffic
from traffic.core import Traffic
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import numpy as np
from geographiclib.geodesic import Geodesic


def origenmismoinstante(datos):
    # pone los datos con el mismo origen independientemente del día
    if not isinstance(datos,Traffic):
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

 


def crearparejas(datos):
    # crea parejas de aviones
    if not isinstance(datos,Traffic):
        datos = Traffic(datos)
    pairs = []
    listado_aves = datos.data.flight_id.unique()
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
    
    columnas = ["alert", "callsign", "hour", "icao24", "last_position", "onground", "spi", "squawk"]
    Datos_fil_ave1 = Datos_ave1.drop(columns = columnas)
    Datos_fil_ave2 = Datos_ave2.drop(columns = columnas)

    # Tenemos que reiniciar los indices para que coincidan
    Datos_fil_ave2.index = range(Datos_fil_ave2.shape[0])
    Datos_fil_ave1.index = range(Datos_fil_ave1.shape[0])

    # Lo vamos ambas en el mismo dataFrame y lo unimos finalmente con el pairs que contienen los pares de aeronaves
    Datos_fil = Datos_fil_ave1.join(Datos_fil_ave2, lsuffix= '_1', rsuffix = '_2')
    Datos_fil = pares.join(Datos_fil)

    # Una vez comproado que funcion vamos a eliminar las columans de flight_id_1 y flight_id_2 para que no se repitan
    Datos_fil = Datos_fil.drop(columns = ['flight_id_1', 'flight_id_2'])
    return Datos_fil

def calculomagnitudesrelativas(datos):
    from math import radians, sqrt, cos, sin

    # Toda la información que necesitamos para ssaber como funciona es https://living-sun.com/es/python/693845-geopy-calculating-gps-heading-bearing-python-python-3x-gps-geo-geopy.html
    def geo_calcs12(lat1,lon1,lat2,lon2):
        return Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['s12']/1852
    def geo_calcsazi1(lat1,lon1,lat2,lon2):
        return Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['azi1']

    datos['Init separation'] = np.vectorize(geo_calcs12)(datos['latitude_1'],datos['longitude_1'],datos['latitude_2'],datos['longitude_2'])
    datos['Init acimut'] = np.vectorize(geo_calcsazi1)(datos['latitude_1'],datos['longitude_1'],datos['latitude_2'],datos['longitude_2'])
  


    def var_track(track1,track2):
        return track1 - track2
    def var_vel(vel1,vel2,track1,track2):
        vel1_x, vel1_y = vel1*cos(radians(90-track1)), vel1 * sin(radians(90-track1))
        vel2_x, vel2_y = vel2*cos(radians(90-track2)), vel2 * sin(radians(90-track2))
        Var_vel = sqrt((vel1_x - vel2_x)**2 + (vel1_y - vel2_y)**2)
        return Var_vel
    datos['Var GS Module'] = np.vectorize(var_vel)(datos['groundspeed_1'],datos['groundspeed_2'],datos['track_1'],datos['track_2'])
    datos['Var Track'] = np.vectorize(var_track)(datos['track_1'],datos['track_2'])
    
    def init_altitude(alt1,alt2):
        return alt1-alt2
    
    def vert_speed(vrate1,vrate2):
        return vrate1 -vrate2
    datos['Var init altitude'] = np.vectorize(init_altitude)(datos['altitude_1'],datos['altitude_2'])
    datos['Var Vertical speed'] = np.vectorize(vert_speed)(datos['vertical_rate_1'],datos['vertical_rate_2'])
    
    return datos

def conflict_detection(CPA_datos):
    # Obtengo las filas en las que la mínima de separacion longitudinal es inferior a 5 MN
    rows_lon = CPA_datos['lateral'] < 5
    CPA_datos_lon = CPA_datos[rows_lon]
    CPA_datos_lon
    # De estas filas obtengo las que se cumple que es menor de 1000 ft la vertical
    rows_vert = CPA_datos_lon['vertical'] < 1000
    CPA_conf = CPA_datos_lon[rows_vert]
    if len(CPA_conf) > 0:
        conf = 1     # Nos da un 1 si hay alguna fila que cumpla ambas condiciones
        Minsep = min(CPA_conf['lateral'])
        # Para calcular el tiempo cogemos el primer instante en el que se genera el conflicto ya que la aeronave entra en el 0000, 
        # En el caso de que la aeronave no entrara en el instante 00 habría que restarlo
        # hora_original = Un problema ya que hay que coger el primer instante en el que entran las aeronaves
        dif_segundos = CPA_conf.iloc[0].timestamp.hour*3600 + CPA_conf.iloc[0].timestamp.minute*60 + CPA_conf.iloc[0].timestamp.second
        Timetoconf = dif_segundos
    else:
        conf = 0     # Nos da un 0 si no hay ninguna fila que cumpla una vulneración de ambas mínimas de separación
        # En el caso de que no haya conflictos ponemos un 10, no podemos poner la minima distancia ya  que quizá dos aeronaves se cruzan 
        #a 3 NM pero con una vertical de 30000 ft y por lo tanto se vuelve loco el algoritmo, también se podría pensar en ponerlo
        Minsep = 10
        # Lo mismo ocurrre con el tiempo
        Timetoconf = 10000 # Hemos puesto 10000 segundos pero sin saber realmente como puede afectar, habría que analizarlo
    return conf, Minsep, Timetoconf


def paresconconflictos(CPA):
    label_ave1, label_ave2 = pd.Series(CPA["flight_id_x"].unique()), pd.Series(CPA["flight_id_y"].unique())
    pairs_CPA = pd.DataFrame({'flight_id_x': label_ave1, 'flight_id_y': label_ave2})
    conflict = []    # Matriz en la que vamos a guardar si hay conflicto o no
    TTC = []         # Matriz en la que vamos a guardar el tiempo al conflicto
    MinDis = []      # Matriz en la que vamos a guardar la distancia mínima alcanzada entre aeronaves

    # Para cada una de las parejas tenemos que obtener la parte del CPA que le corrresponde:
    for index, row in pairs_CPA.iterrows():
        # Sacamos los nombres de cada par de aeronaves
        ave1, ave2 = row['flight_id_x'], row['flight_id_y']
        CPA_1 = CPA[CPA['flight_id_x'] == ave1]
        CPA_datos = CPA_1[CPA_1['flight_id_y'] == ave2]
        # CPA_datos contiene toda la información para un par de aeronaves con conflicto y le aplicamos la función conflicto
        conf, Minsep, Timetoconf = conflict_detection(CPA_datos)
        conflict.append(conf), MinDis.append(Minsep), TTC.append(Timetoconf)

    # Introducimos las variables de variación de altitud y de vertical speed
    pairs_CPA['Conflicto'] = conflict
    pairs_CPA['MinDis'] = MinDis
    pairs_CPA['Timetoconf'] = TTC
    return pairs_CPA

def mod_conflictos(pairs_CPA, Datos_fil_con):
    # identificamos las filas que tienen conflicto
    Datos_final = Datos_fil_con
    rows_conflict = pairs_CPA['Conflicto'] == 1
    pairs_CPA_conflict = pairs_CPA[rows_conflict]
    
    # En el caso de que haya algún conflicto hay que cambiar los 0 por 1, y las distancias por sus valores 
    if len(pairs_CPA_conflict) > 0:
        i = 0
        for index, rows_conflict in pairs_CPA_conflict.iterrows():
            # identifico las aeronaves que tienen conflicto
            ave1_conflict, ave2_conflict = rows_conflict['flight_id_x'], rows_conflict['flight_id_y']
            # Obtenemos la row en la cual hay conflicto
            Datos_fil_con_ave1 = Datos_fil_con[Datos_fil_con['ave1'] == ave1_conflict]
            Datos_fil_con_ave1_ave2 = Datos_fil_con_ave1[Datos_fil_con_ave1['ave2'] == ave2_conflict]
            print(Datos_fil_con_ave1_ave2.index)
            # Identificados la row en la que hay conflicto, tenemos que cambiar el 1 por el 0
            Datos_final['Conflicto'][Datos_fil_con_ave1_ave2.index] = 1
            # Ahora calculamos la mínima distancia que le ocurre a este
            Minsep = pairs_CPA_conflict['MinDis'].iloc[i]
            Datos_final['MinDis'][Datos_fil_con_ave1_ave2.index] = Minsep
            # Lo mismo para el tiempo
            TTC = pairs_CPA_conflict['Timetoconf'].iloc[i]
            Datos_final['Timetoconf'][Datos_fil_con_ave1_ave2.index] = TTC
            # Pongo un contador para las matrices de distancia y tiempo
            i = i + 1
    else:
        Datos_final = Datos_fil_con
    
    return Datos_final


"""
def datosrellenados(datos1,datos2):
    Datos_ave1 = datos1
    Datos_ave2 = datos2
    columnas = ["alert", "callsign", "hour", "icao24", "last_position", "onground", "spi", "squawk"]
    Datos_fil_ave1 = Datos_ave1.drop(columns = columnas)
    Datos_fil_ave2 = Datos_ave2.drop(columns = columnas)

    # Tenemos que reiniciar los indices para que coincidan
    Datos_fil_ave2.index = range(Datos_fil_ave2.shape[0])
    Datos_fil_ave1.index = range(Datos_fil_ave1.shape[0])

    # Lo vamos ambas en el mismo dataFrame y lo unimos finalmente con el pairs que contienen los pares de aeronaves
    Datos_fil = Datos_fil_ave1.join(Datos_fil_ave2, lsuffix= '_1', rsuffix = '_2')
    Datos_fil = pairs.join(Datos_fil)

    # Una vez comproado que funcion vamos a eliminar las columans de flight_id_1 y flight_id_2 para que no se repitan
    Datos_fil = Datos_fil.drop(columns = ['flight_id_1', 'flight_id_2'])
    return Datos_fil


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
    columnas = ["alert", "callsign", "hour", "icao24", "last_position", "onground", "spi", "squawk"]
    Datos_fil_ave1 = Datos_ave1.drop(columns = columnas)
    Datos_fil_ave2 = Datos_ave2.drop(columns = columnas)

    # Tenemos que reiniciar los indices para que coincidan
    Datos_fil_ave2.index = range(Datos_fil_ave2.shape[0])
    Datos_fil_ave1.index = range(Datos_fil_ave1.shape[0])

    # Lo vamos ambas en el mismo dataFrame y lo unimos finalmente con el pairs que contienen los pares de aeronaves
    Datos_fil = Datos_fil_ave1.join(Datos_fil_ave2, lsuffix= '_1', rsuffix = '_2')
    Datos_fil =pairs.join(Datos_fil)

    # Una vez comproado que funcion vamos a eliminar las columans de flight_id_1 y flight_id_2 para que no se repitan
    Datos_fil = Datos_fil.drop(columns = ['flight_id_1', 'flight_id_2'])
    #return Datos_ave1, Datos_ave2
    
    def datosrellenados(datos1,datos2):
    Datos_ave1 = datos1
    Datos_ave2 = datos2
    columnas = ["alert", "callsign", "hour", "icao24", "last_position", "onground", "spi", "squawk"]
    Datos_fil_ave1 = Datos_ave1.drop(columns = columnas)
    Datos_fil_ave2 = Datos_ave2.drop(columns = columnas)

    # Tenemos que reiniciar los indices para que coincidan
    Datos_fil_ave2.index = range(Datos_fil_ave2.shape[0])
    Datos_fil_ave1.index = range(Datos_fil_ave1.shape[0])

    # Lo vamos ambas en el mismo dataFrame y lo unimos finalmente con el pairs que contienen los pares de aeronaves
    Datos_fil = Datos_fil_ave1.join(Datos_fil_ave2, lsuffix= '_1', rsuffix = '_2')
    Datos_fil = pairs.join(Datos_fil)

    # Una vez comproado que funcion vamos a eliminar las columans de flight_id_1 y flight_id_2 para que no se repitan
    Datos_fil = Datos_fil.drop(columns = ['flight_id_1', 'flight_id_2'])
    return Datos_fil
    
def origenmismoinstante(datos):
    # pone los datos con el mismo origen independientemente del día
    if not isinstance(datos,Traffic):
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
"""



