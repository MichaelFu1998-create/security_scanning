def LEVINSON(r, order=None, allow_singularity=False):
    r"""Levinson-Durbin recursion.

    Find the coefficients of a length(r)-1 order autoregressive linear process

    :param r: autocorrelation sequence of length N + 1 (first element being the zero-lag autocorrelation)
    :param order: requested order of the autoregressive coefficients. default is N.
    :param allow_singularity: false by default. Other implementations may be True (e.g., octave)

    :return:
        * the `N+1` autoregressive coefficients :math:`A=(1, a_1...a_N)`
        * the prediction errors
        * the `N` reflections coefficients values

    This algorithm solves the set of complex linear simultaneous equations
    using Levinson algorithm.

    .. math::

        \bold{T}_M \left( \begin{array}{c} 1 \\ \bold{a}_M \end{array} \right) =
        \left( \begin{array}{c} \rho_M \\ \bold{0}_M  \end{array} \right)

    where :math:`\bold{T}_M` is a Hermitian Toeplitz matrix with elements
    :math:`T_0, T_1, \dots ,T_M`.

    .. note:: Solving this equations by Gaussian elimination would
        require :math:`M^3` operations whereas the levinson algorithm
        requires :math:`M^2+M` additions and :math:`M^2+M` multiplications.

    This is equivalent to solve the following symmetric Toeplitz system of
    linear equations

    .. math::

        \left( \begin{array}{cccc}
        r_1 & r_2^* & \dots & r_{n}^*\\
        r_2 & r_1^* & \dots & r_{n-1}^*\\
        \dots & \dots & \dots & \dots\\
        r_n & \dots & r_2 & r_1 \end{array} \right)
        \left( \begin{array}{cccc}
        a_2\\
        a_3 \\
        \dots \\
        a_{N+1}  \end{array} \right)
        =
        \left( \begin{array}{cccc}
        -r_2\\
        -r_3 \\
        \dots \\
        -r_{N+1}  \end{array} \right)

    where :math:`r = (r_1  ... r_{N+1})` is the input autocorrelation vector, and
    :math:`r_i^*` denotes the complex conjugate of :math:`r_i`. The input r is typically
    a vector of autocorrelation coefficients where lag 0 is the first
    element :math:`r_1`.


    .. doctest::

        >>> import numpy; from spectrum import LEVINSON
        >>> T = numpy.array([3., -2+0.5j, .7-1j])
        >>> a, e, k = LEVINSON(T)

    """
    #from numpy import isrealobj
    T0  = numpy.real(r[0])
    T = r[1:]
    M = len(T)

    if order is None:
        M = len(T)
    else:
        assert order <= M, 'order must be less than size of the input data'
        M = order

    realdata = numpy.isrealobj(r)
    if realdata is True:
        A = numpy.zeros(M, dtype=float)
        ref = numpy.zeros(M, dtype=float)
    else:
        A = numpy.zeros(M, dtype=complex)
        ref = numpy.zeros(M, dtype=complex)

    P = T0

    for k in range(0, M):
        save = T[k]
        if k == 0:
            temp = -save / P
        else:
            #save += sum([A[j]*T[k-j-1] for j in range(0,k)])
            for j in range(0, k):
                save = save + A[j] * T[k-j-1]
            temp = -save / P
        if realdata:
            P = P * (1. - temp**2.)
        else:
            P = P * (1. - (temp.real**2+temp.imag**2))
        if P <= 0 and allow_singularity==False:
            raise ValueError("singular matrix")
        A[k] = temp
        ref[k] = temp # save reflection coeff at each step
        if k == 0:
            continue

        khalf = (k+1)//2
        if realdata is True:
            for j in range(0, khalf):
                kj = k-j-1
                save = A[j]
                A[j] = save + temp * A[kj]
                if j != kj:
                    A[kj] += temp*save
        else:
            for j in range(0, khalf):
                kj = k-j-1
                save = A[j]
                A[j] = save + temp * A[kj].conjugate()
                if j != kj:
                    A[kj] = A[kj] + temp * save.conjugate()

    return A, P, ref