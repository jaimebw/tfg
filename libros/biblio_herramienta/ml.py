import numpy as np
import pandas as pd

def dividirdatos(datos, test_ratio):
    np.random.seed(5) # esto es para que siempre genere los mismos
    # genera los data sets de entrenamiento y de prueba
    shuffled_indices = np.random.permutation(len(datos))
    test_set_size = int(len(datos) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return datos.iloc[train_indices], datos.iloc[test_indices]