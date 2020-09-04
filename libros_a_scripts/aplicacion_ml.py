from sklearn.model_selection import train_test_split


X = bbdd.drop(columns = ["Conflicto"],axis =1)
y = bbdd["Conflicto"]
X_train, X_test, y_train, y_test = train_test_split(X , y , stratify = y, test_size = 0.2, random_state = 42)