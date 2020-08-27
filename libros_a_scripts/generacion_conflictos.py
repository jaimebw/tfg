import traffic
import time
import pandas as pd 
import os
from traffic.core import Traffic
import matplotlib.pyplot as plt
import datetime
from geographiclib.geodesic import Geodesic
from biblio_herramienta.herramienta import *
from biblio_herramienta.tratardatos import *
from biblio_herramienta.conflictos import *
start_time = time.time()


"""
Funciones:


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
    # Toda la información que necesitamos para ssaber como funciona es https://living-sun.com/es/python/693845-geopy-calculating-gps-heading-bearing-python-python-3x-gps-geo-geopy.html
    acimut = []
    dist2 = []
    # Tenemos que calcular para cada pareja de aeronaves, es deir para cada fila:
    for index, row in datos.iterrows():
        # Seleccionamos cada una de las posiciones que aparecen en cada fila de aeronaves, en este caso en º y no en radianes
        lat1, lon1 = row['latitude_1'], row['longitude_1']
        lat2, lon2 = row['latitude_2'], row['longitude_2']
        # Aplicamos la formula que nos dice y que nos proporciona todos los datos
        geo_calc = Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)
        # Calculamos los valores de acimut (azi1) y de separacion (dist2)
        dist2.append(geo_calc['s12']/1852)
        acimut.append(geo_calc['azi1'])

    # La variable distance nos permite obtener la distancia en el instante inicial en el que entran las aeronaves (en NM)
    # Introducimos la variable distance en el DataFrame
    datos['Init separation'] = dist2
    datos['Init acimut'] = acimut
    acimut = []
    dist2 = []
    # Tenemos que calcular para cada pareja de aeronaves, es deir para cada fila:
    for index, row in datos.iterrows():
        lat1, lon1 = row['latitude_1'], row['longitude_1']
        lat2, lon2 = row['latitude_2'], row['longitude_2']
        # Aplicamos la formula que nos dice y que nos proporciona todos los datos
        data= Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)
        # Calculamos los valores de acimut (azi1) y de separacion (dist2)
        dist2.append(data['s12']/1852)
        acimut.append(data['azi1'])
    
    # La variable distance nos permite obtener la distancia en el instante inicial en el que entran las aeronaves (en NM)
    # Introducimos la variable distance en el DataFrame
    datos['Init separation'] = dist2
    datos['Init acimut'] = acimut
    from math import radians, sqrt, cos, sin

    Var_vel_mod = []    # Variación de la velocidad en módulo por cada par de aeronaves
    Var_track = []    # Variacion del track entre ambas aeronaves
    # Tenemos que calcular para cada pareja de aeronaves, es deir para cada fila:
    for index, row in datos.iterrows():
        # Seleccionamos cada una de las posiciones que aparecen en cada fila de aeronaves, en este caso en º y no en radianes
        vel1, vel2 = row['groundspeed_1'], row['groundspeed_2']
        track1, track2 = row['track_1'], row['track_2']
        # Calculamos la variación del track de la ave 1 con respecto a la 2
        Var_angle = track1 - track2
        # Calculamos la variación de la velocidad en módulo
        vel1_x, vel1_y = vel1*cos(radians(90-track1)), vel1 * sin(radians(90-track1))
        vel2_x, vel2_y = vel2*cos(radians(90-track2)), vel2 * sin(radians(90-track2))
        Var_vel = sqrt((vel1_x - vel2_x)**2 + (vel1_y - vel2_y)**2)
        # Introducimos los valores de velocidad relativa en módulo y de track
        Var_vel_mod.append(Var_vel)
        Var_track.append(Var_angle)
        # La variable distance nos permite obtener la distancia en el instante inicial en el que entran las aeronaves (en NM)
    # Introducimos la variable distance en el DataFrame
    datos['Var GS Module'] = Var_vel_mod
    datos['Var Track'] = Var_track

    Var_altitude = []    # Variación de la velocidad en módulo por cada par de aeronaves
    Var_Vertical_speed = []    # Variacion del track entre ambas aeronaves
    # Tenemos que calcular para cada pareja de aeronaves, es deir para cada fila:
    for index, row in datos.iterrows():
        # Seleccionamos cada una de las posiciones que aparecen en cada fila de aeronaves
        alt1, alt2 = row['altitude_1'], row['altitude_2']
        hspeed_1, hspeed_2 = row['vertical_rate_1'], row['vertical_rate_2']
        # Calculamos la variación de altitude y de velocidad vertical
        Var_alt = alt1 - alt2
        Var_speed = hspeed_1 - hspeed_2
        # Introducimos los valores de altitud y de velocidad relativa
        Var_altitude.append(Var_alt)
        Var_Vertical_speed.append(Var_speed)

    # Introducimos las variables de variación de altitud y de vertical speed
    datos['Var init altitude'] = Var_altitude
    datos['Var Vertical speed'] = Var_Vertical_speed
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

"""
Script que se ejecuta
"""

carpetaDatos = r'/Users/jaimebowen/OneDrive/TFGSeptiembre/libros/datos_sectores/'
#nombreDatos = r"bilbao_f_cluster.csv"
nombreDatos = r"datos_javi_filtrado.csv"
carpetaImagenes = r"generacion_conflictos/"

vuelos = cargardatos(carpetaDatos,nombreDatos) # se cargan los datos filtrados
vuelosp = vuelos.data.copy() # se copian los datos 
vuelosp = Traffic(vuelosp)
vuelosp = origenmismoinstante(vuelosp) # se les pasa al mismo instante

pairs = crearparejas(vuelosp)

datos_fil = generadorDFconflictos(vuelosp,pairs)
guardarcsv(datos_fil,"datos_f_c_pares_javi")
os.system('say "terminado df conflictos"')
datos_fil = calculomagnitudesrelativas(datos_fil)
guardarcsv(datos_fil,"datos_f_c_pares_relativo_javi")
os.system('say "terminado magnitudes realtivas"')
CPA = vuelosp.closest_point_of_approach(lateral_separation = 10*1852, vertical_separation = 2000)
os.system('say "terminado CPA"')
pairs_CPA = paresconconflictos(CPA)

Datos_fil_con = datos_fil
Datos_fil_con["Conflicto"] = 0
Datos_fil_con["MinDis"] = 10
Datos_fil_con["Timetoconf"] = 10000

BBDD = mod_conflictos(pairs_CPA, Datos_fil_con)
os.system('say "terminado mod conflictos"')
,SCmkp+dvq+opmo     jiqm 
BBDD_2 = BBDD
var_eliminar = ['ave1', 'ave2', 'groundspeed_1', 'timestamp_1', 'vertical_rate_1', 'track_1', 'altitude_2', 'geoaltitude_2',
                'latitude_2', 'longitude_2','timestamp_2','groundspeed_2','track_2','vertical_rate_2']
BBDD_2 = BBDD_2.drop(var_eliminar, axis = 'columns')
guardarcsv(BBDD_2, "BBDD_javi2")
con = BBDD_2.loc[(BBDD_2['Conflicto'] == 1)]
columnas = ['cluster_1', 'cluster_2']
flujos_con_cruce = con[columnas].drop_duplicates()
Flujo_1 = flujos_con_cruce.iloc[0]

BBDD_Flujos = BBDD_2.loc[BBDD_2['cluster_1'] == Flujo_1['cluster_1']]
BBDD_Flujos = BBDD_Flujos.loc[BBDD_2['cluster_2'] == Flujo_1['cluster_2']]

# Si no el siguiente paso sería obtener una matriz para cada uno de los flujos conflictos para que se automatice
# Aquí lo estamos calculando para las aeronaves del flujo 1 con el 0 por ejemplo, pero del 0 al 1 es otro flujo
j = 1
for i, flow in flujos_con_cruce.iterrows():
    # Seleccionamos de la BBDD las filas que cumplen el cluster_1
    filas_1 = BBDD_2.loc[BBDD_2['cluster_1'] == flow['cluster_1']]
    # Seleccionamos del primer filtrado las filas que cumplen el cluster_2
    filas_2 = filas_1.loc[filas_1['cluster_2'] == flow['cluster_2']]
    # Le damos un nombre con un número distinto a cada una de las matrices
    exec('Flujos{} = filas_2'.format(j))
    j = j + 1
# Con este paso ya hemos conseguido programar la subdivisión de los flujos para que lo haga de golpe y nos saquen tantas matrices como necesitamos
print("--- %s seconds ---" % (time.time() - start_time))
