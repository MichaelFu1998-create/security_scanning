def fBrown(H,T,N,M,dW = None,cholesky = False):
    '''
    Sample fractional Brownian motion with differentiability index H 
    on interval [0,T] (H=1/2 yields standard Brownian motion)
    
    :param H: Differentiability, larger than 0
    :param T: Final time
    :param N: Number of time steps
    :param M: Number of samples
    :param dW: Driving noise, optional
    '''
    alpha = 0.5-H
    times = np.linspace(0, T, N)
    dt = T/(N-1)
    if cholesky:
        if dW is not None:
            raise ValueError('Cannot use provided dW if Cholesky method is used')
        times = times[1:]
        tdt = times/np.reshape(times,(-1,1))
        tdt[np.tril_indices(N-1,-1)]=0
        cov = np.reshape(times,(-1,1))**(1-2*alpha)*(1/(1-alpha))*(tdt-1)**(-alpha)*scipy.special.hyp2f1(alpha,1-alpha,2-alpha,1/(1-tdt))
        cov[0,:] = 0
        np.fill_diagonal(cov,times**(1-2*alpha)/(1-2*alpha))
        cov[np.tril_indices(N-1,-1)] = cov.T[np.tril_indices(N-1,-1)]
        L = scipy.linalg.cholesky(cov)
        return np.concatenate((np.zeros((1,M)),L.T@np.random.normal(size=(N-1,M))))
    if dW is None:
        dW = np.sqrt(dt)*np.random.normal(size=(N-1,M))
    if H == 0.5:
        return integral(dF = dW,cumulative = True)  
    a = 1/dt/(1-alpha)*((T-times[N-2::-1])**(1-alpha)-(T-times[:0:-1])**(1-alpha))#a is array that is convolved with dW. Values arise from conditioning integral pieces on dW 
    out = toeplitz_multiplication(a,np.zeros_like(a),dW[::-1])[::-1]
    out -=a[0]*dW#Redo last bit of defining integral with exact simulation below
    cov = np.array([[ dt**(1-2*alpha)/(1-2*alpha),dt**(1-alpha)/(1-alpha)],[dt**(1-alpha)/(1-alpha),dt]])
    var = cov[0,0]-cov[0,1]**2/cov[1,1]
    out += cov[0,1]/cov[1,1]*dW #Conditional mean
    out += np.sqrt(var)*np.random.normal(size = (N-1,M))#Conditional variance
    out = np.concatenate((np.zeros((1,M)),out))
    return out