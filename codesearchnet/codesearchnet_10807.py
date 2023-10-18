def wav2complex(filename):
    """
    Return a complex signal vector from a wav file that was used to store
    the real (I) and imaginary (Q) values of a complex signal ndarray. 
    The rate is included as means of recalling the original signal sample 
    rate.

    fs,x = wav2complex(filename)

    Mark Wickert April 2014
    """
    fs, x_LR_cols = ss.from_wav(filename)
    x = x_LR_cols[:,0] + 1j*x_LR_cols[:,1]
    return fs,x