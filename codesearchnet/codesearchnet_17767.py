def integral(A=None,dF=None,F=None,axis = 0,trapez = False,cumulative = False):
    '''
    Turns an array A of length N (the function values in N points)
    and an array dF of length N-1 (the masses of the N-1 intervals)
    into an array of length N (the integral \int A dF at N points, with first entry 0)
    
    :param A: Integrand (optional, default ones, length N)
    :param dF: Integrator (optional, default ones, length N-1)
    :param F: Alternative to dF (optional, length N)
    :param trapez: Use trapezoidal rule (else left point)
    '''
    ndim = max(v.ndim for v in (A,dF,F) if v is not None)
    def broadcast(x):
        new_shape = [1]*ndim
        new_shape[axis] = -1
        return np.reshape(x,new_shape)
    if F is not None:
        assert(dF is None)
        if F.ndim<ndim:
            F = broadcast(F)
        N = F.shape[axis]
        dF = F.take(indices = range(1,N),axis = axis)-F.take(indices = range(N-1),axis = axis)
    elif dF is not None:
        if dF.ndim<ndim:
            dF = broadcast(dF)
        N = dF.shape[axis]+1
    else:
        if A.ndim<ndim:
            A = broadcast(A)
        N = A.shape[axis]
    if A is not None:
        if trapez:
            midA = (A.take(indices = range(1,N),axis = axis)+A.take(indices = range(N-1),axis = axis))/2
        else:
            midA = A.take(indices=range(N-1),axis=axis)
        if dF is not None:
            dY = midA*dF
        else:
            dY = midA
    else:
        dY = dF
    pad_shape = list(dY.shape)
    pad_shape[axis] = 1
    pad = np.zeros(pad_shape)
    if cumulative:
        return np.concatenate((pad,np.cumsum(dY,axis = axis)),axis = axis)
    else:
        return np.sum(dY,axis = axis)