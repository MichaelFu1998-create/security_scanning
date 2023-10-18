def discount_with_boundaries(X, New, gamma):
    """
    X: 2d array of floats, time x features
    New: 2d array of bools, indicating when a new episode has started
    """
    Y = np.zeros_like(X)
    T = X.shape[0]
    Y[T-1] = X[T-1]
    for t in range(T-2, -1, -1):
        Y[t] = X[t] + gamma * Y[t+1] * (1 - New[t+1])
    return Y