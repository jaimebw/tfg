import traffic
import pandas as pd 
import os
import time
from traffic.core import Traffic
from sklearn.metrics import accuracy_score,f1_score,recall_score,balanced_accuracy_score,precision_score,plot_roc_curve,confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,LabelBinarizer
from sklearn.linear_model import RidgeClassifier,LogisticRegression, SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from biblio_herramienta.herramienta import *
from biblio_herramienta.tratardatos import *
from biblio_herramienta.ml import *

archivoBBDD = r"datos_sectores/BBDD_bilbao.csv"
bbdd = pd.read_csv(archivoBBDD)
cols = [0,1,2,3,4,5,6,8,12,13,16,17,18,21,25,26,19,29,37,38]
bbdd.drop(bbdd.columns[cols],axis=1,inplace= True)

bbdd["Diff lat"] = bbdd["latitude_1"] -bbdd["latitude_2"] 
bbdd["Diff long"] = bbdd["longitude_1"] - bbdd["longitude_2"] 
bbdd["Diff alt"] = bbdd["altitude_1"] - bbdd["altitude_2"] 

X = bbdd.drop(columns = ["Conflicto","altitude_1","altitude_2","latitude_1","latitude_2","longitude_2","longitude_1"],axis =1)
y = bbdd["Conflicto"].to_numpy()
lb = LabelBinarizer()
y = lb.fit_transform(y).ravel()
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X , y , stratify = y, test_size = 0.2, random_state = 42)
####################
# Modelos lineales # 
####################
# Clasificador Ridge

ridge_pipe = Pipeline([
    ('scaler',StandardScaler()),
    ('ridge_classifier',RidgeClassifier(alpha = 0.5))
])


# Clasificador Logísitico

logistic_pipe = Pipeline([
    ('scaler',StandardScaler()),
    ('logistic_classifier',LogisticRegression(random_state = 55))
])

# Clasificador Gradiante Estocastico

sgdc_pipe = Pipeline((
    ('scaler', StandardScaler()),
    ('linear_sgdc', SGDClassifier(random_state = 55)))
)


#pipes = [ridge_pipe ,logistic_pipe ,svm_pipe ,sgdc_pipe , kvecinos_pipe, gauss_pipe, bayes_pipe, arbol_pipe]
lin_pipes = [ridge_pipe ,logistic_pipe ,sgdc_pipe]

nombres_algoritmos_lineal = ["Ridge","Logistico","SGD"]
dlineal = metricas(lin_pipes,X_train, y_train,nombres_algoritmos_lineal)
dlineal.to_csv("modelos_ml/dlineal.csv")
####################
# SVM              # 
####################

from sklearn.svm import LinearSVC,SVC

svm_lineal_pipe = Pipeline((
    ('scaler', StandardScaler()),
    ('linear_svc', LinearSVC(random_state = 55,max_iter=4000))
    
))


svm_pipe = Pipeline((
    ('scaler', StandardScaler()),
    ('svc',SVC(random_state = 55,gamma = "auto"))
))
pipes_svm = [svm_lineal_pipe,svm_pipe ]
start_time = time.time()
pipes_svm_entrenadas=[]
for index, i in enumerate(pipes_svm):
    i.fit(X_train,y_train)
    pipes_svm_entrenadas.append(i)
    
print("--- %s seconds ---" % (time.time() - start_time))
nombres_algoritmos_svm = ["SVM Lineal","SVM Estandar"]
dsvm = metricas(pipes_svm_entrenadas,X_test,y_test,nombres_algoritmos_svm)
dsvm.to_csv("modelos_ml/dsvm.csv")
for i in pipes_svm_entrenadas:
    y_train_pred = cross_val_predict(i, X_train, y_train, cv=7)
    print(confusion_matrix(y_train, y_train_pred))

####################
# Veciones cercanos# 
####################
# Clasificador Veciones cercanos

kvecinos_pipe = Pipeline((
    ('scaler', StandardScaler()),
    ('kveciones_clas', KNeighborsClassifier(weights= "distance"))
))

kvecinos_pipe1 = Pipeline((
    ('scaler', StandardScaler()),
    ('kveciones_clas', KNeighborsClassifier())
))

kvecinos_pipes =[kvecinos_pipe,kvecinos_pipe1]

start_time = time.time()
pipes_kvecinos_entrenadas=[]
for index, i in enumerate(kvecinos_pipes):
    i.fit(X_train,y_train)
    pipes_kvecinos_entrenadas.append(i)
    
print("--- %s seconds ---" % (time.time() - start_time))

nombres_algoritmos_kvecino = ["Vecinos Cercanos Dist","Vecinos Cercanos Weight"]
dkvecinos = metricas(pipes_kvecinos_entrenadas,X_test,y_test,nombres_algoritmos_kvecino)
dkvecinos.to_csv("modelos_ml/dvcerca.csv")

for i in pipes_kvecinos_entrenadas:
    y_train_pred = cross_val_predict(i, X_train, y_train, cv=7)
    print(confusion_matrix(y_train, y_train_pred))


####################
# Bayes            # 
####################
bayes_pipe = Pipeline((
    ('scaler', StandardScaler()),
    ('naive_class', GaussianNB()))
)
bayes_pipes = [bayes_pipe]

nombres_algoritmos_bayes = ["Naive-Bayes gaussiano"]
dbayes = metricas(bayes_pipes,X_train, y_train,nombres_algoritmos_bayes)
dbayes.to_csv("modelos_ml/dbayes.csv")

pipes_bayes_entrenados=[]
for index, i in enumerate(bayes_pipes):
    i.fit(X_train,y_train)
    pipes_bayes_entrenados.append(i)

for i in bayes_pipes :
    y_train_pred = cross_val_predict(i, X_train, y_train, cv=7)
    print(confusion_matrix(y_train, y_train_pred))

plot_roc_curve(pipes_bayes_entrenados[0], X_test, y_test)

####################
#   Arbol          # 
####################
arbol_pipe = Pipeline((
    ('scaler', StandardScaler()),
    ('arbol_class', DecisionTreeClassifier(random_state=55,)))
)
arbol_pipes = [arbol_pipe]
start_time = time.time()
pipes_arbol_entrenados=[]
for index, i in enumerate(arbol_pipes ):
    i.fit(X_train,y_train)
    pipes_arbol_entrenados.append(i)
    
print("--- %s seconds ---" % (time.time() - start_time))
nombres_algoritmos_arbol = ["Arbol"]
darbol= metricas(pipes_arbol_entrenados,X_test,y_test,nombres_algoritmos_arbol )
darbol.to_csv("modelos_ml/darbol2.csv")
for i in pipes_arbol_entrenados:
    y_train_pred = cross_val_predict(i, X_train, y_train, cv=7)
    print(confusion_matrix(y_train, y_train_pred))

plot_roc_curve(pipes_arbol_entrenados[0], X_test, y_test)

####################
#   Neurona         # 
####################

neurona_pipe =  Pipeline((
    ('scaler', StandardScaler()),
    ('neurona_class', MLPClassifier(random_state=55)))
)
neurona_pipe_mod =  Pipeline((
    ('scaler', StandardScaler()),
    ('neurona_class', MLPClassifier(random_state=55,hidden_layer_sizes =(400,) ))
))

neurona_pipes = [neurona_pipe, neurona_pipe_mod]
start_time = time.time()
neurona_pipes_entrenados=[]
for index, i in enumerate(neurona_pipes):
    i.fit(X_train,y_train)
    neurona_pipes_entrenados.append(i)
    
print("--- %s seconds ---" % (time.time() - start_time))

nombres_algoritmos_neurona = ["Neurona estandar","Neurona mod"]
dneurona= metricas(neurona_pipes_entrenados,X_test,y_test,nombres_algoritmos_neurona )
dneurona.to_csv("modelos_ml/dneurona.csv")
for i in neurona_pipes_entrenados:
    y_train_pred = cross_val_predict(i, X_train, y_train, cv=7)
    print(confusion_matrix(y_train, y_train_pred))