def print_profile(function):
    '''
    Decorator that prints memory and runtime information at each call of the function
    '''
    import memory_profiler
    def wrapper(*args,**kwargs):
        m=StringIO()
        pr=cProfile.Profile()
        pr.enable()
        temp_func = memory_profiler.profile(func=function,stream=m,precision=4)
        output = temp_func(*args,**kwargs)
        print(m.getvalue())
        pr.disable()
        ps = pstats.Stats(pr)
        ps.sort_stats('cumulative').print_stats('(?!.*memory_profiler.*)(^.*$)',20)
        m.close()
        return output
    return wrapper