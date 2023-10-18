def objective(param_scales=(1, 1), xstar=None, seed=None):
    """Gives objective functions a number of dimensions and parameter range

    Parameters
    ----------
    param_scales : (int, int)
        Scale (std. dev.) for choosing each parameter

    xstar : array_like
        Optimal parameters
    """
    ndim = len(param_scales)

    def decorator(func):

        @wraps(func)
        def wrapper(theta):
            return func(theta)

        def param_init():
            np.random.seed(seed)
            return np.random.randn(ndim,) * np.array(param_scales)

        wrapper.ndim = ndim
        wrapper.param_init = param_init
        wrapper.xstar = xstar

        return wrapper

    return decorator