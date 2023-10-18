def ex6_2(n):
    """
    Generate a triangle pulse as described in Example 6-2
    of Chapter 6.
    
    You need to supply an index array n that covers at least [-2, 5]. 
    The function returns the hard-coded signal of the example.
    
    Parameters
    ----------
    n : time index ndarray covering at least -2 to +5.
    
    Returns
    -------
    x : ndarray of signal samples in x
    
    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from sk_dsp_comm import sigsys as ss
    >>> n = np.arange(-5,8)
    >>> x = ss.ex6_2(n)
    >>> plt.stem(n,x) # creates a stem plot of x vs n
    """
    x = np.zeros(len(n))
    for k, nn in enumerate(n):
        if nn >= -2 and nn <= 5:
            x[k] = 8 - nn
    return x