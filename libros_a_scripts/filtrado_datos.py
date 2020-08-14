import traffic
from traffic.core import Traffic
import pandas as pd
from biblio_herramienta.tratardatos import *
import numpy as np


carpetaDatos = r'datos_sectores/'
nombreDatos = "datos_bilbao.csv"

vuelos_sintratar = cargardatos(carpetaDatos,nombreDatos) # carga los datos desde el archivo .csv
# se copian los datos en otra variable para no cargarlos de nuevo desde el archivo .csv
vuelos_prueba = vuelos.data.copy()  # este comando copia los datos
vuelos_prueba = traffic.core.Traffic(vuelos_prueba) # este comando los transforma en un objeto de traffic

# elimina las aeronaves en tierra
aviones_entierra =  vuelos_prueba.data[vuelos_prueba.data["onground"] == True].index
vuelos_prueba.data.drop(aviones_entierra,inplace = True)
# elimina las aeronaves que tiene VR distinta de cero
vuelos_prueba.data.drop(aviones_cambiandoFL,inplace = True)
aviones_cambiandoFL = vuelos_prueba.data[vuelos_prueba.data["vertical_rate"]!= 0.0].index 
# elimina las aeronaves que está debajo del FL 345
aviones_debajosector = vuelos_prueba.data[vuelos_prueba.data["altitude"] <= 34500].index
vuelos_prueba.data.drop(aviones_debajosector,inplace = True)

vuelos_prueba = vuelos_prueba.clean_invalid()
vuelos_prueba = vuelos_prueba.drop_duplicates()

# Variables que tienen huecos:
Var_huecos = vuelos_prueba.data.columns[vuelos_prueba.data.isnull().any()]
# Identificar las filas que tienen Nan:
nan_rows = vuelos_prueba.data[vuelos_prueba.data.isnull().any(1)]

# Identificar las aeronaves que tienen problemas con esto:
ave_huecos = nan_rows.callsign.value_counts()

# se identifican las aeronaves que tienen más de 10 datos ads-b con fallos
v_filtrado = vuelos_prueba
for count, values in enumerate(ave_huecos):
    if values > 10:
        list_ave.append(ave_huecos.index[count])
        # se identifican las filas de las aeronaves y las eliminamos
        rows = vuelos_prueba.data.loc[vuelos_prueba.data.callsign == ave_huecos.index[count]].index
        v_filtrado = v_filtrado.drop(rows)



# Eliminamos todas las filas que tienen NaN
v_filtrado = v_filtrado.data.dropna()
v_filtrado = traffic.core.Traffic(v_filtrado)


# Vamos a rellenar los huecos que faltan con la introducción del valor medio. 
# Variables que tienen huecos:
Var_huecos = []
# Detectar las aeronaves que tienen huecos
aves_huecos = []

# Construimos el método impute con las características que queremos para rellenar las celdas
from sklearn.impute import SimpleImputer
my_imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

#Aplicamos el método a cada aeronave:
for count, name in enumerate(aves_huecos):
    ave_impute = pd.DataFrame(my_imputer.fit_transform(vuelos_prueba))

Var_time = ["hour", "last_position", "timestamp"]
v_filtrado1[Var_time] = v_filtrado.data[Var_time] = v_filtrado.data[Var_time].astype("datetime64[ns, UTC]")

guardarcsv(v_filtrado,"datos_filtrados",carpetaDatos)
