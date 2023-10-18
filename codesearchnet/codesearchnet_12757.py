def get_cartesian(r, theta):
    """
    Given a radius and theta, return the cartesian (x, y) coordinates.
    """
    x = r*np.sin(theta)
    y = r*np.cos(theta)

    return x, y