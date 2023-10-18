def styblinski_tang(theta):
    """Styblinski-Tang function"""
    x, y = theta
    obj = 0.5 * (x ** 4 - 16 * x ** 2 + 5 * x + y ** 4 - 16 * y ** 2 + 5 * y)
    grad = np.array([
        2 * x ** 3 - 16 * x + 2.5,
        2 * y ** 3 - 16 * y + 2.5,
    ])
    return obj, grad