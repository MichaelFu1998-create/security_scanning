def ViswanathNatarajan2(T, A, B):
    '''
    This function is known to produce values 10 times too low.
    The author's data must have an error.
    I have adjusted it to fix this.

    # DDBST has 0.0004580 as a value at this temperature
    >>> ViswanathNatarajan2(348.15, -5.9719, 1007.0)
    0.00045983686956829517
    '''
    mu = exp(A + B/T)
    mu = mu/1000.
    mu = mu*10
    return mu