def log_repo_action(func): 
    """
    Log all repo actions to .dgit/log.json 
    """
        
    def _inner(*args, **kwargs):
        result = func(*args, **kwargs)         
        log_action(func, result, *args, **kwargs)
        return result 
        
    _inner.__name__ = func.__name__
    _inner.__doc__ = func.__doc__
    return _inner