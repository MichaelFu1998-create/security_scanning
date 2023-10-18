def rosenbrock(theta):
    """Objective and gradient for the rosenbrock function"""
    x, y = theta
    obj = (1 - x)**2 + 100 * (y - x**2)**2

    grad = np.zeros(2)
    grad[0] = 2 * x - 400 * (x * y - x**3) - 2
    grad[1] = 200 * (y - x**2)
    return obj, grad