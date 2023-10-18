def michalewicz(theta):
    """Michalewicz function"""
    x, y = theta
    obj = - np.sin(x) * np.sin(x ** 2 / np.pi) ** 20 - \
        np.sin(y) * np.sin(2 * y ** 2 / np.pi) ** 20

    grad = np.array([
        - np.cos(x) * np.sin(x ** 2 / np.pi) ** 20 - (40 / np.pi) * x *
        np.sin(x) * np.sin(x ** 2 / np.pi) ** 19 * np.cos(x ** 2 / np.pi),
        - np.cos(y) * np.sin(2 * y ** 2 / np.pi) ** 20 - (80 / np.pi) * y * np.sin(y) *
        np.sin(2 * y ** 2 / np.pi) ** 19 * np.cos(2 * y ** 2 / np.pi),
    ])

    return obj, grad