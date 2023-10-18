def matyas(theta):
    """Matyas function"""
    x, y = theta
    obj = 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y
    grad = np.array([0.52 * x - 0.48 * y, 0.52 * y - 0.48 * x])
    return obj, grad