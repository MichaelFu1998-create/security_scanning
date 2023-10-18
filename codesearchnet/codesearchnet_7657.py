def rlevinson(a, efinal):
    """computes the autocorrelation coefficients, R based
    on the prediction polynomial A and the final prediction error Efinal,
    using the stepdown algorithm.

    Works for real or complex data

    :param a:
    :param efinal:

    :return:
        * R, the autocorrelation
        * U  prediction coefficient
        * kr reflection coefficients
        * e errors

    A should be a minimum phase polynomial and A(1) is assumed to be unity.

    :returns: (P+1) by (P+1) upper triangular matrix, U,
        that holds the i'th order prediction polynomials
        Ai, i=1:P, where P is the order of the input
        polynomial, A.



             [ 1  a1(1)*  a2(2)* ..... aP(P)  * ]
             [ 0  1       a2(1)* ..... aP(P-1)* ]
       U  =  [ .................................]
             [ 0  0       0      ..... 1        ]

    from which the i'th order prediction polynomial can be extracted
    using Ai=U(i+1:-1:1,i+1)'. The first row of U contains the
    conjugates of the reflection coefficients, and the K's may be
    extracted using, K=conj(U(1,2:end)).

    .. todo:: remove the conjugate when data is real data, clean up the code
       test and doc.

    """
    a = numpy.array(a)
    realdata = numpy.isrealobj(a)


    assert a[0] == 1, 'First coefficient of the prediction polynomial must be unity'

    p = len(a)

    if p < 2:
        raise ValueError('Polynomial should have at least two coefficients')

    if realdata == True:
        U = numpy.zeros((p, p)) # This matrix will have the prediction
                                # polynomials of orders 1:p
    else:
        U = numpy.zeros((p, p), dtype=complex)
    U[:, p-1] = numpy.conj(a[-1::-1]) # Prediction coefficients of order p

    p = p -1
    e = numpy.zeros(p)

    # First we find the prediction coefficients of smaller orders and form the
    # Matrix U

    # Initialize the step down

    e[-1] = efinal # Prediction error of order p

    # Step down
    for k in range(p-1, 0, -1):
        [a, e[k-1]] = levdown(a, e[k])
        U[:, k] = numpy.concatenate((numpy.conj(a[-1::-1].transpose()) ,
                                      [0]*(p-k) ))




    e0 = e[0]/(1.-abs(a[1]**2)) #% Because a[1]=1 (true polynomial)
    U[0,0] = 1                #% Prediction coefficient of zeroth order
    kr = numpy.conj(U[0,1:])     #% The reflection coefficients
    kr = kr.transpose()                 #% To make it into a column vector

    #   % Once we have the matrix U and the prediction error at various orders, we can
    #  % use this information to find the autocorrelation coefficients.

    R = numpy.zeros(1, dtype=complex)
    #% Initialize recursion
    k = 1
    R0 = e0 # To take care of the zero indexing problem
    R[0] = -numpy.conj(U[0,1])*R0   # R[1]=-a1[1]*R[0]

    # Actual recursion
    for k in range(1,p):
        r = -sum(numpy.conj(U[k-1::-1,k])*R[-1::-1]) - kr[k]*e[k-1]
        R = numpy.insert(R, len(R), r)

    # Include R(0) and make it a column vector. Note the dot transpose

    #R = [R0 R].';
    R = numpy.insert(R, 0, e0)
    return R, U, kr, e