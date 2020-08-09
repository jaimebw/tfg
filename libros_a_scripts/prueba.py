"""
Este libro contiene las pruebas para poder usar de manera correcta traffic y 
poder configurarlo acorde a lo necesario para el TFG
"""
import traffic
print("Funciona la librería")
from traffic.data import opensky
print("Esta es la ubicación del archivo de configuración: \n")
traffic.config_file
flight = opensky.history(
    "2017-02-05",
    # stop is implicit, i.e. stop="2017-02-06"
    callsign="EZY158T",
    return_flight=True
)
from traffic.data import nm_airspaces
nm_airspaces['LECMBLU']
import matplotlib.pyplot as plt
from traffic.drawing import EuroPP, countries

with plt.style.context('traffic'):
    fig = plt.figure()
    ax = plt.axes(projection=EuroPP())

    ax.add_feature(countries())
    ax.gridlines()
    ax.set_extent((-10, 10.1, 37, 45))

    nm_airspaces['LECMBLU'].plot(ax, lw=2, alpha=1)
    
print("Si se ha ejectuado hasta aquí, se ha configurado todo a la perfección")