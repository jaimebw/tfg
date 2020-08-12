import traffic
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
        # saca el numero de aeronaves en la BBDD
    try:
        numero = df.data["callsign"].nunique()
        print("El numero de aeronaves es de ",numero)
    except:
        print("La BBDD no está correctamente configurada")