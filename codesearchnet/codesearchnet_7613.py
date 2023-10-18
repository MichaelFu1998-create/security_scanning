def tf2zp(b,a):
    """Convert transfer function filter parameters to zero-pole-gain form

    Find the zeros, poles, and gains of this continuous-time system:

    .. warning:: b and a must have the same length.

    ::

    
        from spectrum import tf2zp
        b = [2,3,0]
        a = [1, 0.4, 1]
        [z,p,k] = tf2zp(b,a)          % Obtain zero-pole-gain form
        z =
            1.5
            0
        p =
           -0.2000 + 0.9798i
            -0.2000 - 0.9798i
        k =
           2

    :param b: numerator
    :param a: denominator
    :param fill: If True, check that the length of a and b are the same. If not, create a copy of the shortest element and append zeros to it.
    :return: z (zeros), p (poles), g (gain)


    Convert transfer function f(x)=sum(b*x^n)/sum(a*x^n) to
    zero-pole-gain form f(x)=g*prod(1-z*x)/prod(1-p*x)

    .. todo:: See if tf2ss followed by ss2zp gives better results.  These
        are available from the control system toolbox.  Note that
        the control systems toolbox doesn't bother, but instead uses

    .. seealso:: scipy.signal.tf2zpk, which gives the same results but uses a different
        algorithm (z^-1 instead of z).
    """
    from numpy import roots
    assert len(b) == len(a), "length of the vectors a and b must be identical. fill with zeros if needed."

    g = b[0] / a[0]
    z = roots(b)
    p = roots(a)

    return z, p, g