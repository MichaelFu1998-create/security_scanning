def computeGaussKernel(x):
    """Compute the gaussian kernel on a 1D vector."""
    xnorm = np.power(euclidean_distances(x, x), 2)
    return np.exp(-xnorm / (2.0))