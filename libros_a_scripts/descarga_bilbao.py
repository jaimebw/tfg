from traffic.data import opensky,nm_airspaces #se importan los recursos que se van a usar


flight = opensky.history(
    "2019-02-05", # fecha de inicia
    "2019-02-08", # fecha de parada
    # stop is implicit, i.e. stop="2017-02-06"
    return_flight=True, # define la clase de estructura en función de lo que se necesita
    bounds= nm_airspaces['LECMBLU'] # area de descarga de los datos
)    