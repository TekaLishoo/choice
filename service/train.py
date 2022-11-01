from sklearn.neighbors import KNeighborsClassifier


def train_and_predict(X, y, others):
    neigh = KNeighborsClassifier(n_neighbors=4)
    neigh.fit(X, y)
    return neigh.predict_proba(others)
