def generator_to_list(function):
    """
    Wrap a generator function so that it returns a list when called.
    
    For example:
        
        # Define a generator
        >>> def mygen(n):
        ...     i = 0
        ...     while i < n:
        ...         yield i
        ...         i += 1
        # This is how it might work
        >>> generator = mygen(5)
        >>> generator.next()
        0
        >>> generator.next()
        1
        # Wrap it in generator_to_list, and it will behave differently.
        >>> mygen = generator_to_list(mygen)
        >>> mygen(5)
        [0, 1, 2, 3, 4]
    """
    
    def wrapper(*args, **kwargs):
        return list(function(*args, **kwargs))
    wrapper.__name__ = function.__name__
    wrapper.__doc__ = function.__doc__
    return wrapper