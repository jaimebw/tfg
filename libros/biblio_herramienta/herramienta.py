
def guardarcsv(archivo, nombre_archivo,carpeta_datos_csv ):
    # esta funciona genera una carpeta sino existe, y guarda los datos descargados en esta
    if not os.path.exists(carpeta_datos_csv):
        os.mkdir(carpeta_datos_csv)
    # guarda el archivo .csv en la carpeta especificada
    carpeta_datos_csv = r"datos_sectores/"
    archivo.to_csv(carpeta_datos_csv+nombre_archivo+".csv")

def probartraffic():
    # prueba si las bibliotecas está bien instaladas
    try:
        import traffic
        print("Traffic instalado")
    except:
        print("La librería no esta correctamente instalada")

def cargardatos(carpeta,nombre_datos):
    # carga los datos descargados desde una carpeta
    datos_cargados = traffic.core.Traffic.from_file(carpeta+nombre_datos)
    return datos_cargados

def niveldevuelo(altitud_metros):
    # devuelve el nivel de vuelo 
    try:
        fl = altitud_metros*3.28/1000
        return fl
    except:
        pass

def numeroaeronavesector(df):
    import traffic
        # saca el numero de aeronaves en la BBDD
    try:
        numero = df.data["callsign"].nunique()
        print("El numero de aeronaves es de ",numero)
    except:
        print("La BBDD no está correctamente configurada")

def representartrayectoria(traffic_data,sector ='LECMBLU'):
    # esta funcion representa las trayectorias dentro de la BBDD sobre el sector que se estudiar
    import matplotlib.pyplot as plt
    from traffic.core.projection import EuroPP
    from traffic.data import nm_airspaces
    from traffic.drawing import countries
    with plt.style.context("traffic"):
        fig, ax = plt.subplots(
            subplot_kw=dict(projection=EuroPP()))
        nm_airspaces[sector].plot(ax,alpha = 1)
        ax.add_feature(countries())
        ax.set_extent((-6, 1, 40, 50))
        traffic_data.plot(ax,alpha = 0.2)