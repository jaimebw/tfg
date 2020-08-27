import traffic
import pandas as pd 
import os
from traffic.core import Traffic
from biblio_herramienta.herramienta import *
from biblio_herramienta.tratardatos import *

carpetaDatos = r'datos_sectores/' # carpeta que contiene los datos
nombreDatos = "datos_filtrados_def.csv"
carpetaImagenes = r"filtrado_cluster/"
vuelos = cargardatos(carpetaDatos,nombreDatos)
vuelos

vuelos = vuelos.assign_id().unwrap().eval(max_workers=4)
vuelos.data.head()

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from traffic.core.projection import CH1903

# la funcion permite aplicar algoritmos de ML a los datos que tenemos
vuelos_dbscan = vuelos.clustering(
    nb_samples=15, # divide en 15 puntos las trayecorias
    features=["longitude", "latitude", "track_unwrapped"], # datos cebados al algorimto de ML
    clustering=DBSCAN(eps=0.5, min_samples=10), # algoritmo de ML utilizado, con los parámetros del mismo
    transform=StandardScaler(), # lo que hace esto es escalar los datos dentro de una distribuciñ¡ón Gausiana
).fit_predict()

representarcluster(vuelos_dbscan,"cluster_dbscan.png","filtrado_cluster/")

lusters = (-1, 0, 1, 5, 7,8, 10, 11 , 12) # se resta uno dado que se cuentan desde cero, y el -1 que es el total de las trayectorias
#vuelos_dbscan_F = pd.DataFrame()
for i in clusters:
    aviones_fuera_sector = vuelos_dbscan_f[vuelos_dbscan_f["cluster"]== int(i)].index
    vuelos_dbscan_f.drop(aviones_fuera_sector,inplace = True)

vuelos_dbscan_f = Traffic(vuelos_dbscan_f)
guardarcsv(vuelos_dbscan_f,"bilbao_f_cluster")
representarSobreSector(vuelos_dbscan_f)
guardarimagen(carpetaImagenes,"sector_filtrado.png")