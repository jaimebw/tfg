import traffic
from traffic.core import Traffic

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
