def HERMTOEP(T0, T, Z):
    """solve Tx=Z by a variation of Levinson algorithm where T 
    is a complex hermitian toeplitz matrix

    :param T0: zero lag value
    :param T: r1 to rN
     
    :return: X
    
    used by eigen PSD method
    """
    assert len(T)>0
    M = len(T)
    X = numpy.zeros(M+1,dtype=complex)
    A = numpy.zeros(M,dtype=complex)
    P = T0
    if P == 0: raise ValueError("P must be different from zero")
    X[0] = Z[0]/T0 
    for k in range(0, M):
        save = T[k]
        beta = X[0]*T[k]
        if k == 0:
            temp = -save / P
        else:
            for j in range(0, k):
                save = save + A[j] * T[k-j-1]
                beta = beta + X[j+1] * T[k-j-1]
            temp = -save / P
        P = P * (1. - (temp.real**2+temp.imag**2))
        if P <= 0:
            raise ValueError("singular matrix")
        A[k] = temp
        alpha = (Z[k+1]-beta)/P

        if k == 0:
            #print 'skipping code for k=0' 
            X[k+1] = alpha
            for j in range(0,k+1):
                X[j] = X[j] + alpha * A[k-j].conjugate()
            continue
        khalf = (k+1)//2
        for j in range(0, khalf):
            kj = k-j-1
            save=A[j]
            A[j] = save+temp*A[kj].conjugate() 
            if j != kj:
                A[kj] = A[kj] + temp*save.conjugate()
        X[k+1] = alpha
        for j in range(0,k+1):
            X[j] = X[j] + alpha * A[k-j].conjugate()
    return X