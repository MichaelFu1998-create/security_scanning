def cache(func):
    """
    Caches results of a call to a grid function. If a grid that evaluates to the same byte value is passed into the same
    function of the same instance as previously then the cached result is returned.

    Parameters
    ----------
    func
        Some instance method that takes a grid as its argument

    Returns
    -------
    result
        Some result, either newly calculated or recovered from the cache
    """

    def wrapper(instance: GeometryProfile, grid: np.ndarray, *args, **kwargs):
        if not hasattr(instance, "cache"):
            instance.cache = {}
        key = (func.__name__, grid.tobytes())
        if key not in instance.cache:
            instance.cache[key] = func(instance, grid)
        return instance.cache[key]

    return wrapper