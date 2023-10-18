def black_scholes(times,r,sigma,S0,d,M,dW=None):
    '''
    Return M Euler-Maruyama sample paths with N time steps of S_t, where 
        dS_t = S_t*r*dt+S_t*sigma*dW_t
        S(0)=S0
    
    :rtype: M x N x d array
    '''
    N=len(times)
    times = times.flatten()
    p0 = np.log(S0)
    if dW is None:
        dW=np.sqrt(times[1:]-times[:-1])[None,:,None]*np.random.normal(size=(M,N-1,d))
    if np.squeeze(sigma).ndim<=1:
        dF = sigma*dW
        ito_correction = np.squeeze(sigma**2/2)
    else:
        dF = np.einsum('ij,...j',sigma,dW)
        ito_correction = np.sum(sigma**2,1)/2
    drift  = (r-ito_correction)*times[None,:,None]
    diffusion = integral(dF=dF,axis=1,cumulative = True)
    return np.exp(p0 + drift + diffusion)