def heston(times,mu,rho,kappa,theta,xi,S0,nu0,d,M,nu_1d=True):
    '''
    Return M Euler-Maruyama sample paths with N time steps of (S_t,v_t), where
        (S_t,v_t) follows the Heston model of mathematical finance

    :rtype: M x N x d array
    '''
    d_nu = 1 if nu_1d else d
    nu = np.zeros((M,len(times),d_nu))
    S = np.zeros((M,len(times),d))
    nu[:,0,:] = nu0
    S[:,0,:] = S0
    if 2*kappa*theta<=xi**2:
        raise ValueError('Feller condition not satisfied')
    test = np.std(np.diff(times.flatten())) 
    if test>1e-12:
        raise ValueError
    dt = times[1]-times[0]
    N = len(times)
    if d == 1:
        if np.array(rho).size ==1:
            rho = np.array([[1,rho],[rho,1]])
    chol = np.linalg.cholesky(rho)
    dW = np.sqrt(dt)*np.einsum('ij,...j',chol,np.random.normal(size=(M,N-1,d+d_nu)))
    for i in range(1,N):
        dt = times[i]-times[i-1]
        nu[:,i,:] = np.abs(nu[:,i-1,:] + kappa*(theta-nu[:,i-1,:])*dt+xi*np.sqrt(nu[:,i-1,:])*dW[:,i-1,d:])
    S = S0*np.exp(integral(np.sqrt(nu),dF = dW[:,:,:d],axis=1,cumulative = True)+integral(mu - 0.5*nu,F = times,axis=1,trapez=False,cumulative = True))
    return np.concatenate((S,nu),axis=-1)