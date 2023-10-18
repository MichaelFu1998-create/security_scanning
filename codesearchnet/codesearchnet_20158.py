def booth(theta):
    """Booth's function"""
    x, y = theta

    A = x + 2 * y - 7
    B = 2 * x + y - 5
    obj = A**2 + B**2
    grad = np.array([2 * A + 4 * B, 4 * A + 2 * B])
    return obj, grad