def checkCAS(CASRN):
    '''Checks if a CAS number is valid. Returns False if the parser cannot 
    parse the given string..

    Parameters
    ----------
    CASRN : string
        A three-piece, dash-separated set of numbers

    Returns
    -------
    result : bool
        Boolean value if CASRN was valid. If parsing fails, return False also.

    Notes
    -----
    Check method is according to Chemical Abstract Society. However, no lookup
    to their service is performed; therefore, this function cannot detect
    false positives.

    Function also does not support additional separators, apart from '-'.
    
    CAS numbers up to the series 1 XXX XXX-XX-X are now being issued.
    
    A long can hold CAS numbers up to 2 147 483-64-7

    Examples
    --------
    >>> checkCAS('7732-18-5')
    True
    >>> checkCAS('77332-18-5')
    False
    '''
    try:
        check = CASRN[-1]
        CASRN = CASRN[::-1][1:]
        productsum = 0
        i = 1
        for num in CASRN:
            if num == '-':
                pass
            else:
                productsum += i*int(num)
                i += 1
        return (productsum % 10 == int(check))
    except:
        return False