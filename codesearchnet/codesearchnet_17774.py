def print_memory(function):
    '''
    Decorator that prints memory information at each call of the function
    '''
    import memory_profiler
    def wrapper(*args,**kwargs):
        m = StringIO()
        temp_func = memory_profiler.profile(func = function,stream=m,precision=4)
        output = temp_func(*args,**kwargs)
        print(m.getvalue())
        m.close()
        return output
    return wrapper