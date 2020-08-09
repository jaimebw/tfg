from traffic.data import opensky 
import os 
carpeta_datos_csv = r"datos_sectores/
def guardarcsv(archivo, nombre_archivo,carpeta_datos_csv = carpeta_datos_csv):
    # esta funciona genera una carpeta sino existe, y guarda los datos descargados en esta
    if not os.path.exists(carpeta_datos_csv):
        os.mkdir(carpeta_datos_csv)
    # guarda el archivo .csv en la carpeta especificada
    carpeta_datos_csv = r"datos_sectores/"
    archivo.to_csv(carpeta_datos_csv+nombre_archivo+".csv")
    
flight = opensky.history(
    "2017-02-05", # día para descargar 
    callsign="EZY158T", # indicador del vuelo
    return_flight=True # devuelve las datos como un objeto de FLIGHT
)
guardarcsv(flight,"datos_prueba",carpeta_datos_csv)
flight
import matplotlib.pyplot as plt
from traffic.drawing import EuroPP, PlateCarree, countries, rivers
with plt.style.context('traffic'):
    fig, ax = plt.subplots(
        subplot_kw=dict(projection=EuroPP())
    )
    ax.add_feature(countries())
    ax.add_feature(rivers())
    ax.set_extent((-7, 13, 42, 50))

    # no specific method for that in traffic
    # but switch back to pandas DataFrame for manual plot
    flight.data.plot.scatter(
            ax=ax, x='longitude', y='latitude',
            transform=PlateCarree(), s=5, cmap='viridis'
    )