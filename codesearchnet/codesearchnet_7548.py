def _swapsides(data):
    """todo is it really useful ?

    Swap  sides

    .. doctest::

        >>> from spectrum import swapsides
        >>> x = [-2, -1, 1, 2]
        >>> swapsides(x)
        array([ 2, -2, -1])

    """
    N = len(data)
    return np.concatenate((data[N//2+1:], data[0:N//2]))