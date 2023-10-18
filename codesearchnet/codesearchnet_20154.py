def doublewell(theta):
    """Pointwise minimum of two quadratic bowls"""
    k0, k1, depth = 0.01, 100, 0.5
    shallow = 0.5 * k0 * theta ** 2 + depth
    deep = 0.5 * k1 * theta ** 2
    obj = float(np.minimum(shallow, deep))
    grad = np.where(deep < shallow, k1 * theta, k0 * theta)
    return obj, grad