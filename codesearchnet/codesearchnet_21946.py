def chisquare(observe, expect, error, ddof, verbose=True):
    """
    Finds the reduced chi square difference of *observe* and *expect* with a given *error* and *ddof* degrees of freedom.

    *verbose* flag determines if the reduced chi square is printed to the terminal. 
    """
    chisq = 0
    error   = error.flatten()
    observe = observe.flatten()
    expect  = expect.flatten()
    for i, el in enumerate(observe):
        chisq = chisq + _np.power((el - expect[i]) / error[i], 2)

    red_chisq = chisq / (len(observe) - ddof)
    if verbose:
        # print 'Chi-Squared is {}.'.format(chisq)
        print('Reduced Chi-Squared is {}.'.format(red_chisq))

    return red_chisq