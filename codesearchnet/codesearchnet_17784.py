def r_bergomi(H,T,eta,xi,rho,S0,r,N,M,dW=None,dW_orth=None,cholesky = False,return_v=False):
    '''
    Return M Euler-Maruyama sample paths with N time steps of (S_t,v_t), where
        (S_t,v_t) follows the rBergomi model of mathematical finance

    :rtype: M x N x d array
    '''
    times = np.linspace(0, T, N)
    dt = T/(N-1)
    times = np.reshape(times,(-1,1))
    if dW is None:
        dW = np.sqrt(dt)*np.random.normal(size=(N-1,M))
    if dW_orth is None:
        dW_orth = np.sqrt(dt)*np.random.normal(size=(N-1,M))
    dZ = rho*dW+np.sqrt(1-rho**2)*dW_orth
    Y = eta*np.sqrt(2*H)*fBrown(H,T,N,M,dW =dW,cholesky = cholesky)
    v = xi*np.exp(Y-0.5*(eta**2)*times**(2*H))
    S = S0*np.exp(integral(np.sqrt(v),dF = dZ,axis=0,cumulative = True)+integral(r - 0.5*v,F = times,axis=0,trapez=False,cumulative = True))
    if return_v:
        return np.array([S,v]).T
    else:
        return np.array([S]).T