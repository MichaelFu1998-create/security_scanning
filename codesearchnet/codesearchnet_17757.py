def chain(*fs):
    '''
    Concatenate functions
    '''
    def chained(x):
        for f in reversed(fs):
            if f:
                x=f(x)
        return x
    return chained