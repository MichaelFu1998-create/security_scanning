def zakharov(theta):
    """Zakharov function"""
    x, y = theta
    obj = x ** 2 + y ** 2 + (0.5 * x + y) ** 2 + (0.5 * x + y) ** 4
    grad = np.array([
        2.5 * x + y + 2 * (0.5 * x + y) ** 3,
        4 * y + x + 4 * (0.5 * x + y) ** 3,
    ])
    return obj, grad