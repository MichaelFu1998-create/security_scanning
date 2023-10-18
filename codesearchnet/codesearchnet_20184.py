def sdcone(x, rho):
    """Projection onto the semidefinite cone"""
    U, V = np.linalg.eigh(x)
    return V.dot(np.diag(np.maximum(U, 0)).dot(V.T))