def dixon_price(theta):
    """Dixon-Price function"""
    x, y = theta
    obj = (x - 1) ** 2 + 2 * (2 * y ** 2 - x) ** 2
    grad = np.array([
        2 * x - 2 - 4 * (2 * y ** 2 - x),
        16 * (2 * y ** 2 - x) * y,
    ])
    return obj, grad