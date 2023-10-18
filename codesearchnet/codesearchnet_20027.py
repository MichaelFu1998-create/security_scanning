def timeit(timer=None):
    """simple timer. returns a time object, or a string."""
    if timer is None:
        return time.time()
    else:
        took=time.time()-timer
        if took<1:
            return "%.02f ms"%(took*1000.0)
        elif took<60:
            return "%.02f s"%(took)
        else:
            return "%.02f min"%(took/60.0)