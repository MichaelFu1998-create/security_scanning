def uniform_noise(points):
    """Init a uniform noise variable."""
    return np.random.rand(1) * np.random.uniform(points, 1) \
        + random.sample([2, -2], 1)