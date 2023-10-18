def mccormick(theta):
    """McCormick function"""
    x, y = theta
    obj = np.sin(x + y) + (x - y)**2 - 1.5 * x + 2.5 * y + 1
    grad = np.array([np.cos(x + y) + 2 * (x - y) - 1.5,
                     np.cos(x + y) - 2 * (x - y) + 2.5])
    return obj, grad