def print_runtime(function):
    '''
    Decorator that prints running time information at each call of the function
    '''
    def wrapper(*args,**kwargs):
        pr=cProfile.Profile()
        pr.enable()
        output = function(*args,**kwargs)
        pr.disable()
        ps = pstats.Stats(pr)
        ps.sort_stats('tot').print_stats(20)
        return output
    return wrapper