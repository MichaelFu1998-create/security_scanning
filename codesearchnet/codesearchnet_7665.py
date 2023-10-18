def corrmtx(x_input, m, method='autocorrelation'):
    r"""Correlation matrix

    This function is used by PSD estimator functions. It generates
    the correlation matrix from a correlation data set and a maximum lag.

    :param array x: autocorrelation samples (1D)
    :param int m: the maximum lag

    Depending on the choice of the method, the correlation matrix has different
    sizes, but the number of rows is always m+1.

    Method can be :

    * 'autocorrelation': (default) X is the (n+m)-by-(m+1) rectangular Toeplitz
      matrix derived using prewindowed and postwindowed data.
    * 'prewindowed': X is the n-by-(m+1) rectangular Toeplitz matrix derived
      using prewindowed data only.
    * 'postwindowed': X is the n-by-(m+1) rectangular Toeplitz matrix that
      derived using postwindowed data only.
    * 'covariance': X is the (n-m)-by-(m+1) rectangular Toeplitz matrix
      derived using nonwindowed data.
    * 'modified': X is the 2(n-m)-by-(m+1) modified rectangular Toeplitz
      matrix that generates an autocorrelation estimate for the length n data
      vector x, derived using forward and backward prediction error estimates.


    :return:
        * the autocorrelation matrix
        * R, the (m+1)-by-(m+1) autocorrelation matrix estimate ``R= X'*X``.

    .. rubric:: Algorithm details:

    The **autocorrelation** matrix is a :math:`(N+p) \times (p+1)` rectangular Toeplilz
    data matrix:

    .. math:: X_p = \begin{pmatrix}L_p\\T_p\\Up\end{pmatrix}

    where the lower triangular :math:`p \times (p+1)` matrix :math:`L_p` is

    .. math:: L_p =
        \begin{pmatrix}
        x[1]     &  \cdots     & 0     & 0        \\
        \vdots    &  \ddots     & \vdots & \vdots    \\
        x[p]     &  \cdots     & x[1]  & 0
        \end{pmatrix}

    where the rectangular :math:`(N-p) \times (p+1)` matrix :math:`T_p` is

    .. math:: T_p =
        \begin{pmatrix}
        x[p+1]     &  \cdots    & x[1]        \\
        \vdots    &  \ddots     & \vdots    \\
        x[N-p]     &  \cdots    & x[p+1]        \\
        \vdots    &  \ddots     & \vdots    \\
        x[N]     &  \cdots      & x[N-p]
        \end{pmatrix}

    and where the upper triangular :math:`p \times (p+1)` matrix :math:`U_p` is

    .. math:: U_p =
        \begin{pmatrix}
        0         &  x[N]      & \cdots     & x[N-p+1]        \\
        \vdots    &  \vdots    & \ddots & \vdots    \\
        0         &  0         & \cdots  & x[N]
        \end{pmatrix}

    From this definition, the prewindowed matrix is

    .. math:: X_p = \begin{pmatrix}L_p\\T_p\end{pmatrix}

    the postwindowed matrix is

    .. math:: X_p = \begin{pmatrix}T_p\\U_p\end{pmatrix}

    the covariance matrix is:

    .. math:: X_p = \begin{pmatrix}T_p\end{pmatrix}

    and the modified covariance matrix is:

    .. math:: X_p = \begin{pmatrix}T_p\\T_p^*\end{pmatrix}


    """

    valid_methods = ['autocorrelation', 'prewindowed', 'postwindowed',
                      'covariance', 'modified']
    if method not in valid_methods:
        raise ValueError("Invalid method. Try one of %s" % valid_methods)

    from scipy.linalg import toeplitz

    # create the relevant matrices that will be useful to create
    # the correlation matrices
    N = len(x_input)

    # FIXME:do we need a copy ?
    if isinstance(x_input, list):
        x = numpy.array(x_input)
    else:
        x = x_input.copy()


    if x.dtype == complex:
        complex_type = True
    else:
        complex_type = False

    # Compute the Lp, Up and Tp matrices according to the requested method
    if method in ['autocorrelation', 'prewindowed']:
        Lp = toeplitz(x[0:m], [0]*(m+1))
    Tp = toeplitz(x[m:N], x[m::-1])
    if method in ['autocorrelation', 'postwindowed']:
        Up = toeplitz([0]*(m+1), numpy.insert(x[N:N-m-1:-1],0,0))



    # Create the output matrix

    if method == 'autocorrelation':
        if complex_type == True:
            C = numpy.zeros((N+m, m+1), dtype=complex)
        else:
            C = numpy.zeros((N+m, m+1))
        for i in range(0, m):
            C[i] = Lp[i]
        for i in range(m, N):
            C[i] = Tp[i-m]
        for i in range(N, N+m):
            C[i] = Up[i-N]
    elif method == 'prewindowed':
        if complex_type == True:
            C = numpy.zeros((N, m+1), dtype=complex)
        else:
            C = numpy.zeros((N, m+1))

        for i in range(0, m):
            C[i] = Lp[i]
        for i in range(m, N):
            C[i] = Tp[i-m]
    elif method == 'postwindowed':
        if complex_type == True:
            C = numpy.zeros((N, m+1), dtype=complex)
        else:
            C = numpy.zeros((N, m+1))
        for i in range(0, N-m):
            C[i] = Tp[i]
        for i in range(N-m, N):
            C[i] = Up[i-N+m]
    elif method == 'covariance':
        return Tp
    elif method == 'modified':
        if complex_type == True:
            C = numpy.zeros((2*(N-m), m+1), dtype=complex)
        else:
            C = numpy.zeros((2*(N-m), m+1))
        for i in range(0, N-m):
            C[i] = Tp[i]
        Tp = numpy.fliplr(Tp.conj())
        for i in range(N-m, 2*(N-m)):
            C[i] = Tp[i-N+m]



    return C