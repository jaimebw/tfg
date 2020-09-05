import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve,precision_recall_curve
from sklearn.model_selection import cross_val_predict
import matplotlib.pyplot as plt


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

