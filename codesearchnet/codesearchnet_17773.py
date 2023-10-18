def add_runtime(function):
    '''
    Decorator that adds a runtime profile object to the output
    '''
    def wrapper(*args,**kwargs):  
        pr=cProfile.Profile()
        pr.enable()
        output = function(*args,**kwargs)
        pr.disable()
        return pr,output
    return wrapper