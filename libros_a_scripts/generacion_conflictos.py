
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