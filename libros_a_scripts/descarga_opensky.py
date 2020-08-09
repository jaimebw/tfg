from traffic.data import opensky # se importan los recursos 
                                 # que se van a usar


flight = opensky.history(
    "2017-02-05", # día para descargar 
    callsign="EZY158T", # indicador del vuelo
    return_flight=True # devuelve las datos como un objeto de FLIGHT
)
