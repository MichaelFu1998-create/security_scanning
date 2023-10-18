def sos_zplane(sos,auto_scale=True,size=2,tol = 0.001):
    """
    Create an z-plane pole-zero plot.

    Create an z-plane pole-zero plot using the numerator
    and denominator z-domain system function coefficient
    ndarrays b and a respectively. Assume descending powers of z.

    Parameters
    ----------
    sos : ndarray of the sos coefficients
    auto_scale : bool (default True)
    size : plot radius maximum when scale = False

    Returns
    -------
    (M,N) : tuple of zero and pole counts + plot window
    
    Notes
    -----
    This function tries to identify repeated poles and zeros and will 
    place the multiplicity number above and to the right of the pole or zero.
    The difficulty is setting the tolerance for this detection. Currently it
    is set at 1e-3 via the function signal.unique_roots.

    Examples
    --------
    >>> # Here the plot is generated using auto_scale
    >>> sos_zplane(sos)
    >>> # Here the plot is generated using manual scaling
    >>> sos_zplane(sos,False,1.5)
    """
    Ns,Mcol = sos.shape
    # Extract roots from sos num and den removing z = 0
    # roots due to first-order sections
    N_roots = []
    for k in range(Ns):
        N_roots_tmp = np.roots(sos[k,:3])
        if N_roots_tmp[1] == 0.:
            N_roots = np.hstack((N_roots,N_roots_tmp[0]))
        else:
            N_roots = np.hstack((N_roots,N_roots_tmp))
    D_roots = []
    for k in range(Ns):
        D_roots_tmp = np.roots(sos[k,3:])
        if D_roots_tmp[1] == 0.:
            D_roots = np.hstack((D_roots,D_roots_tmp[0]))
        else:
            D_roots = np.hstack((D_roots,D_roots_tmp))
    # Plot labels if multiplicity greater than 1
    x_scale = 1.5*size
    y_scale = 1.5*size   
    x_off = 0.02
    y_off = 0.01
    M = len(N_roots)
    N = len(D_roots)
    if auto_scale:
        if M > 0 and N > 0:
            size = max(np.max(np.abs(N_roots)),np.max(np.abs(D_roots)))+.1
        elif M > 0:
            size = max(np.max(np.abs(N_roots)),1.0)+.1
        elif N > 0:
            size = max(1.0,np.max(np.abs(D_roots)))+.1
        else:
            size = 1.1
    plt.figure(figsize=(5,5))
    plt.axis('equal')
    r = np.linspace(0,2*np.pi,200)
    plt.plot(np.cos(r),np.sin(r),'r--')
    plt.plot([-size,size],[0,0],'k-.')
    plt.plot([0,0],[-size,size],'k-.')
    if M > 0:
        #N_roots = np.roots(b)
        N_uniq, N_mult=unique_cpx_roots(N_roots,tol=tol)
        plt.plot(np.real(N_uniq),np.imag(N_uniq),'ko',mfc='None',ms=8)
        idx_N_mult = np.nonzero(np.ravel(N_mult>1))[0]
        for k in range(len(idx_N_mult)):
            x_loc = np.real(N_uniq[idx_N_mult[k]]) + x_off*x_scale
            y_loc =np.imag(N_uniq[idx_N_mult[k]]) + y_off*y_scale
            plt.text(x_loc,y_loc,str(N_mult[idx_N_mult[k]]),
                     ha='center',va='bottom',fontsize=10)
    if N > 0:
        #D_roots = np.roots(a)
        D_uniq, D_mult=unique_cpx_roots(D_roots,tol=tol)
        plt.plot(np.real(D_uniq),np.imag(D_uniq),'kx',ms=8)
        idx_D_mult = np.nonzero(np.ravel(D_mult>1))[0]
        for k in range(len(idx_D_mult)):
            x_loc = np.real(D_uniq[idx_D_mult[k]]) + x_off*x_scale
            y_loc =np.imag(D_uniq[idx_D_mult[k]]) + y_off*y_scale
            plt.text(x_loc,y_loc,str(D_mult[idx_D_mult[k]]),
                     ha='center',va='bottom',fontsize=10)            
    if M - N < 0:
        plt.plot(0.0,0.0,'bo',mfc='None',ms=8)
    elif M - N > 0:
        plt.plot(0.0,0.0,'kx',ms=8)
    if abs(M - N) > 1:
        plt.text(x_off*x_scale,y_off*y_scale,str(abs(M-N)),
                 ha='center',va='bottom',fontsize=10)        
    plt.xlabel('Real Part')
    plt.ylabel('Imaginary Part')
    plt.title('Pole-Zero Plot')
    #plt.grid()
    plt.axis([-size,size,-size,size])
    return M,N