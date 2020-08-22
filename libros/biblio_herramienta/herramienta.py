import traffic
from traffic.core import Traffic
import matplotlib.pyplot as plt
from itertools import islice, cycle
from traffic.drawing import countries, EuroPP
from traffic.data import nm_airspaces
from .tratardatos import guardarimagen
import numpy as np
from sklearn.impute import SimpleImputer

def probartraffic():
    # prueba si las bibliotecas está bien instaladas
    try:
        import traffic
        import sklearn
        print("Traffic instalado")
    except:
        print("La librería no esta correctamente instalada")


def representarSobreSector(traffic_data,sector ='LECMBLU'):
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
        
        
def ejesespaña():
    return (-6,0, 42.7, 44.5)

def filtrardatos(datos):
    if not isinstance(datos,Traffic):
        datos = Traffic(datos)
    # condiciones del sector
    aviones_entierra =  datos.data[datos.data["onground"] == True].index 
    datos.data.drop(aviones_entierra,inplace = True)
    aviones_debajosector = datos.data[datos.data["altitude"] <= 34500].index
    datos.data.drop(aviones_debajosector,inplace = True)
    

    # filtrado de datos no validos
    datos = datos.clean_invalid()
    datos = datos.drop_duplicates()

    # filtrado de datos incompletos
    Var_huecos = datos.data.columns[datos.data.isnull().any()]
    # identificacion de filas con NaN
    nan_rows = datos.data[datos.data.isnull().any(1)]

    # identificacion de aeronaves con NaN
    ave_huecos = nan_rows.callsign.value_counts()
    list_ave = []
    # identificacion de aeronaves con >10 fallos de recepción ADS-B
    v_filtrado = datos
    for count, values in enumerate(ave_huecos):
        if values > 10:
            list_ave.append(ave_huecos.index[count])
            # se identifican las filas de las aeronaves y las eliminamos
            rows = datos.data.loc[datos.data.callsign == ave_huecos.index[count]].index
            v_filtrado = v_filtrado.drop(rows)

    # se eliminan todas las filas que tienen NaN
    v_filtrado = v_filtrado.data.dropna() # OJO devuelve un df no un Traffic
    v_filtrado = traffic.core.Traffic(v_filtrado)
    Var_huecos = []
    # identificación de aeronaves con huecos
    aves_huecos = []
    # se cambian los nans por la media enter los dos valores
    from sklearn.impute import SimpleImputer
    my_imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

    #Aplicamos el método a cada aeronave:
    for count, name in enumerate(aves_huecos):
        ave_impute = pd.DataFrame(my_imputer.fit_transform(vuelos_prueba))
    return v_filtrado





    


"""
def representarcluster(datos_cluster,nombre_cluster):
    # esta funcion representa el cluster, y lo guarda en una imagen
    n_clusters = 1 + datos_cluster.data.cluster.max() 
    color_cycle = cycle(
        "#a6cee3 #1f78b4 #b2df8a #33a02c #fb9a99 #e31a1c "
        "#fdbf6f #ff7f00 #cab2d6 #6a3d9a #ffff99 #b15928".split()
    )
    colors = list(islice(color_cycle, n_clusters)) 
    colors.append("#aaaaaa") 
    
    nb_cols = 3
    nb_lines = (1 + n_clusters) // nb_cols + (((1 + n_clusters) % nb_cols) > 0)
    
    with plt.style.context("traffic"):
        
  
        fig, ax = plt.subplots(
            nb_lines, nb_cols, figsize=(10, 15), subplot_kw=dict(projection=EuroPP())
            # parametros de la figura y de los ejes
        )

        for cluster in range(-1, n_clusters):
            ax_ = ax[(cluster + 1) // nb_cols][(cluster + 1) % nb_cols]
            ax_.add_feature(countries())
            nm_airspaces['LECMBLU'].plot(ax_,alpha = 1)

            datos_cluster.query(f"cluster == {cluster}").plot(
                ax_, color=colors[cluster], alpha=0.1 if cluster == -1 else 1
            )
            # la funcion de arriba busca la asginación de cluster
            ax_.set_global()
            ax_.set_extent(nm_airspaces['LECMBLU'])
            if cluster == -1:
                ax_.title.set_text("Conjunto")
            else:
                ax_.title.set_text("Cluster = " +str(cluster) )

    guardarimagen("imagenes_cluster",nombre_cluster)   
"""


def representarcluster(datos_cluster,nombre_cluster,iskmeans = False):
    # esta funcion representa el cluster, y lo guarda en una imagen
    n_clusters = 1 + datos_cluster.data.cluster.max() 
    color_cycle = cycle(
        "#a6cee3 #1f78b4 #b2df8a #33a02c #fb9a99 #e31a1c "
        "#fdbf6f #ff7f00 #cab2d6 #6a3d9a #ffff99 #b15928".split()
    )
    colors = list(islice(color_cycle, n_clusters)) 
    colors.append("#aaaaaa") 
    
    nb_cols = 3
    nb_lines = (1 + n_clusters) // nb_cols + (((1 + n_clusters) % nb_cols) > 0)
    
    with plt.style.context("traffic"):
        
  
        fig, ax = plt.subplots(
            nb_lines, nb_cols, figsize=(10, 15), subplot_kw=dict(projection=EuroPP())
            # parametros de la figura y de los ejes
        )
        if iskmeans == True:
            for cluster in range(0, n_clusters):
                ax_ = ax[(cluster + 1) // nb_cols][(cluster + 1) % nb_cols]
                ax_.add_feature(countries())
                nm_airspaces['LECMBLU'].plot(ax_,alpha = 1)

                datos_cluster.query(f"cluster == {cluster}").plot(
                    ax_, color=colors[cluster], alpha=0.1 if cluster == -1 else 1
                )
        else:
            for cluster in range(-1, n_clusters):
                ax_ = ax[(cluster + 1) // nb_cols][(cluster + 1) % nb_cols]
                ax_.add_feature(countries())
                nm_airspaces['LECMBLU'].plot(ax_,alpha = 1)

                datos_cluster.query(f"cluster == {cluster}").plot(
                    ax_, color=colors[cluster], alpha=0.1 if cluster == -1 else 1
                )
            # la funcion de arriba busca la asginación de cluster
                ax_.set_global()
                ax_.set_extent(nm_airspaces['LECMBLU'])
                if cluster == -1:
                    ax_.title.set_text("Conjunto")
                else:
                    ax_.title.set_text("Cluster = " +str(cluster) )

    guardarimagen("imagenes_cluster",nombre_cluster)