def bohachevsky1(theta):
    """One of the Bohachevsky functions"""
    x, y = theta
    obj = x ** 2 + 2 * y ** 2 - 0.3 * np.cos(3 * np.pi * x) - 0.4 * np.cos(4 * np.pi * y) + 0.7
    grad = np.array([
        2 * x + 0.3 * np.sin(3 * np.pi * x) * 3 * np.pi,
        4 * y + 0.4 * np.sin(4 * np.pi * y) * 4 * np.pi,
    ])
    return obj, grad