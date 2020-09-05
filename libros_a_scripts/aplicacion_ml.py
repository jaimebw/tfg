from sklearn.model_selection import train_test_split


X = bbdd.drop(columns = ["Conflicto"],axis =1)
y = bbdd["Conflicto"]
X_train, X_test, y_train, y_test = train_test_split(X , y , stratify = y, test_size = 0.2, random_state = 42)

nombreAlgoritmo_pipe = Pipeline([
    ('scaler',nombre_del_preprocesador),
    ('algoritmo',nombre_algoritmo(hiperparametros))

])

nombreAlgoritmo_pipe.fit(X_train,y_train)

# Medidores para el algoritmo 

accuracy_score(y_true, y_pred)

cross_val_score(sgd_clf, X_train, y_train_5, cv=3, scoring="accuracy")
cross_val_score(pipeline, X_train, y_train, cv, scoring)
confusion_matrix(y_train, y_train_pred)
curvaROC(pipe,X_train,y_train)