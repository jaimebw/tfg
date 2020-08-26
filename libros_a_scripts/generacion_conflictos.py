import traffic
import pandas as pd 
import os
from traffic.core import Traffic
from biblio_herramienta.herramienta import *
from biblio_herramienta.tratardatos import *
from biblio_herramienta.conflictos import *

carpetaDatos = r'datos_sectores/' # carpeta que contiene los datos
nombreDatos = r"bilbao_f_cluster.csv"
#nombreDatos = r"datos_javi_filtrado.csv"
carpetaImagenes = r"generacion_conflictos/"

vuelos = cargardatos(carpetaDatos,nombreDatos) # se cargan los datos filtrados
vuelosp = vuelos.data.copy() # se copian los datos 
vuelosp = Traffic(vuelosp)
vuelosp = origenmismoinstante(vuelosp) # se les pasa al mismo instante

pairs = crearparejas(vuelosp)

datos_fil = generadorDFconflictos(vuelosp,pairs)

datos_fil = calculomagnitudesrelativas(datos_fil)

CPA = vuelos.closest_point_of_approach(lateral_separation = 10*1852, vertical_separation = 2000)

pairs_CPA = paresconconflictos(CPA)

Datos_fil_con = datos_fil
Datos_fil_con["Conflicto"] = 0
Datos_fil_con["MinDis"] = 10
Datos_fil_con["Timetoconf"] = 10000

BBDD = mod_conflictos(pairs_CPA, Datos_fil_con)

BBDD_2 = BBDD
var_eliminar = ['ave1', 'ave2', 'groundspeed_1', 'timestamp_1', 'vertical_rate_1', 'track_1', 'altitude_2', 'geoaltitude_2',
                'latitude_2', 'longitude_2','timestamp_2','groundspeed_2','track_2','vertical_rate_2']
BBDD_2 = BBDD_2.drop(var_eliminar, axis = 'columns')

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



"""
timestamp = pd.Series([])
listado_aves = datos.data.flight_id.unique()
for ave in listado_aves:
    # se selecciona la trayectoria de la aeronave
    tray = datos[ave].data
    tray2 = tray
    # se selecciona el instante inicial
    init_time = tray.timestamp.iloc[0]
    # se resta el instante inicial al resto de los puntos agrupados en la trayectoria
    tray2_timestamp = tray.timestamp - datetime.timedelta(hours = init_time.hour, minutes = init_time.minute, seconds = init_time.second)
    timestamp = timestamp.append(tray2_timestamp)

datos.data.timestamp = timestamp
datos.data.info()


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
Datos_fil = pairs.join(Datos_fil)

# Una vez comproado que funcion vamos a eliminar las columans de flight_id_1 y flight_id_2 para que no se repitan
Datos_fil = Datos_fil.drop(columns = ['flight_id_1', 'flight_id_2'])

CPA = vuelos.closest_point_of_approach(lateral_separation = 10*1852, vertical_separation = 2000)
pairs_CPA = paresconconflictos(CPA)
"""