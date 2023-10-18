def set_mkl_thread_limit(cores):
    """
    set mkl thread limit and return old value so we can reset
    when finished. 
    """
    if "linux" in sys.platform:
        mkl_rt = ctypes.CDLL('libmkl_rt.so')
    else:
        mkl_rt = ctypes.CDLL('libmkl_rt.dylib')
    oldlimit = mkl_rt.mkl_get_max_threads()
    mkl_rt.mkl_set_num_threads(ctypes.byref(ctypes.c_int(cores)))
    return oldlimit