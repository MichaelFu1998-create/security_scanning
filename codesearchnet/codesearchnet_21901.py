def scatter(obj, axis=-1, blocksize=None):
    """Distribute obj or list to remote engines, returning proxy objects
    Args:
      obj: any python object, or list of objects
      axis (int, optional): Can be used if scattering a numpy array,
        specifying along which axis to split the array to distribute it. The 
        default is to split along the last axis. `None` means do not distribute
      blocksize (int, optional): Can be used if scattering a numpy array. 
        Optionally control the size of intervals into which the distributed
        axis is split (the default splits the distributed axis evenly over all
        computing engines).
    """
    if hasattr(obj, '__distob_scatter__'):
        return obj.__distob_scatter__(axis, None, blocksize)
    if distob._have_numpy and (isinstance(obj, np.ndarray) or
                        hasattr(type(obj), '__array_interface__')):
        return _scatter_ndarray(obj, axis, blocksize)
    elif isinstance(obj, Remote):
        return obj
    ars = _async_scatter(obj)
    proxy_obj = _ars_to_proxies(ars)
    return proxy_obj