import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve,precision_recall_curve,accuracy_score,f1_score,recall_score,balanced_accuracy_score,precision_score
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt

def metricas(pipes_lin_entrenadas,X_test, y_test,nombre_algoritmos):
    exactitud_lineales = []
    exactitud_lineales_b = []
    sensibilidad_lineales = []
    precision_lineales = []
    f1_lineales = []
    for i in pipes_lin_entrenadas:
        precision_lineales.append(precision_score(y_test,i.predict(X_test)))
        exactitud_lineales.append(accuracy_score(y_test,i.predict(X_test)))
        f1_lineales.append(f1_score(y_test,i.predict(X_test)))
        sensibilidad_lineales.append(recall_score(y_test,i.predict(X_test)))
    clasificadores = pd.DataFrame({"Clasificador":nombre_algoritmos,"Exactitud":exactitud_lineales,"Precision":precision_lineales,"Sensibilidad":sensibilidad_lineales,"F1":f1_lineales})
    return clasificadores

def curvaROC(pipe,X_train,y_train):
    # representa la curva roc
    y_scores = cross_val_predict(pipe, X_train, y_train, cv=3,
                                 method="decision_function")

    fpr, tpr, thresholds = roc_curve(y_train, y_scores)


    def plot_roc_curve(fpr, tpr, label=None):
        plt.plot(fpr, tpr, linewidth=2, label=label)
        plt.plot([0, 1], [0, 1], 'k--')
        plt.axis([0, 1, 0, 1])
        plt.xlabel('Ratio de Falsos Positivos')
        plt.ylabel('Ratio de Verdaderos Positivos')

    plot_roc_curve(fpr, tpr)
    plt.show()
    

def plot_precision_recall_vs_threshold(pipe,X_train,y_train):
    y_scores = cross_val_predict(svm_pipe, X_train, y_train, cv=3,
                                 method="decision_function")
    precisions, recalls, thresholds = precision_recall_curve(y_train, y_scores)
    plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
    plt.plot(thresholds, recalls[:-1], "g-", label="Recall")
    plt.xlabel("Threshold")
    plt.legend(loc="center left")
    plt.ylim([0, 1])
    plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
    plt.show()

