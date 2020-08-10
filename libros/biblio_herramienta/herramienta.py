def guardarcsv(archivo, nombre_archivo,carpeta_datos_csv ):
    # esta funciona genera una carpeta sino existe, y guarda los datos descargados en esta
    if not os.path.exists(carpeta_datos_csv):
        os.mkdir(carpeta_datos_csv)
    # guarda el archivo .csv en la carpeta especificada
    carpeta_datos_csv = r"datos_sectores/"
    archivo.to_csv(carpeta_datos_csv+nombre_archivo+".csv")

def probartraffic():
    try:
        import traffic
        print("Traffic instalado")
    except:
        print("La librería no esta correctamente instalada")
