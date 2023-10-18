def check_cuda_devices():
    """Output some information on CUDA-enabled devices on your computer,
    including current memory usage. Modified to only get number of devices.

    It's a port of https://gist.github.com/f0k/0d6431e3faa60bffc788f8b4daa029b1
    from C to Python with ctypes, so it can run without compiling
    anything. Note that this is a direct translation with no attempt to
    make the code Pythonic. It's meant as a general demonstration on how
    to obtain CUDA device information from Python without resorting to
    nvidia-smi or a compiled Python extension.


    .. note:: Author: Jan Schlüter, https://gist.github.com/63a664160d016a491b2cbea15913d549.git
    """
    import ctypes

    # Some constants taken from cuda.h
    CUDA_SUCCESS = 0

    libnames = ('libcuda.so', 'libcuda.dylib', 'cuda.dll')
    for libname in libnames:
        try:
            cuda = ctypes.CDLL(libname)
        except OSError:
            continue
        else:
            break
    else:
        # raise OSError("could not load any of: " + ' '.join(libnames))
        return 0

    nGpus = ctypes.c_int()
    error_str = ctypes.c_char_p()

    result = cuda.cuInit(0)
    if result != CUDA_SUCCESS:
        cuda.cuGetErrorString(result, ctypes.byref(error_str))
        # print("cuInit failed with error code %d: %s" % (result, error_str.value.decode()))
        return 0
    result = cuda.cuDeviceGetCount(ctypes.byref(nGpus))
    if result != CUDA_SUCCESS:
        cuda.cuGetErrorString(result, ctypes.byref(error_str))
        # print("cuDeviceGetCount failed with error code %d: %s" % (result, error_str.value.decode()))
        return 0
    # print("Found %d device(s)." % nGpus.value)
    return nGpus.value