import traffic
from traffic.core import Traffic
import matplotlib.pyplot as plt
from itertools import islice, cycle
from traffic.drawing import countries, EuroPP
from traffic.data import nm_airspaces
from .tratardatos import guardarimagen


def probartraffic():
    # prueba si las bibliotecas está bien instaladas
    try:
        import traffic
        print("Traffic instalado")
    except:
        print("La librería no esta correctamente instalada")

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