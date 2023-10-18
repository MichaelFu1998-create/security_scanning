def argmax(l,f=None):
    """http://stackoverflow.com/questions/5098580/implementing-argmax-in-python"""
    if f:
        l = [f(i) for i in l]
    return max(enumerate(l), key=lambda x:x[1])[0]