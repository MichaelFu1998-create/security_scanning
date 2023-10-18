def beale(theta):
    """Beale's function"""
    x, y = theta
    A = 1.5 - x + x * y
    B = 2.25 - x + x * y**2
    C = 2.625 - x + x * y**3
    obj = A ** 2 + B ** 2 + C ** 2
    grad = np.array([
        2 * A * (y - 1) + 2 * B * (y ** 2 - 1) + 2 * C * (y ** 3 - 1),
        2 * A * x + 4 * B * x * y + 6 * C * x * y ** 2
    ])
    return obj, grad