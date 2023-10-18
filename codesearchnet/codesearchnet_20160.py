def camel(theta):
    """Three-hump camel function"""
    x, y = theta
    obj = 2 * x ** 2 - 1.05 * x ** 4 + x ** 6 / 6 + x * y + y ** 2
    grad = np.array([
        4 * x - 4.2 * x ** 3 + x ** 5 + y,
        x + 2 * y
    ])
    return obj, grad