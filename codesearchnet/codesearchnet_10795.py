def splane(b,a,auto_scale=True,size=[-1,1,-1,1]):
    """
    Create an s-plane pole-zero plot.
    
    As input the function uses the numerator and denominator 
    s-domain system function coefficient ndarrays b and a respectively. 
    Assumed to be stored in descending powers of s.
    
    Parameters
    ----------
    b : numerator coefficient ndarray. 
    a : denominator coefficient ndarray. 
    auto_scale : True 
    size : [xmin,xmax,ymin,ymax] plot scaling when scale = False 
    
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
    >>> splane(b,a)
    >>> # Here the plot is generated using manual scaling
    >>> splane(b,a,False,[-10,1,-10,10])
    """
    M = len(b) - 1
    N = len(a) - 1
    plt.figure(figsize=(5,5))
    #plt.axis('equal')
    N_roots = np.array([0.0])
    if M > 0:
        N_roots = np.roots(b)
    D_roots = np.array([0.0])
    if N > 0:
        D_roots = np.roots(a)
    if auto_scale:
        size[0] = min(np.min(np.real(N_roots)),np.min(np.real(D_roots)))-0.5
        size[1] = max(np.max(np.real(N_roots)),np.max(np.real(D_roots)))+0.5
        size[1] = max(size[1],0.5)
        size[2] = min(np.min(np.imag(N_roots)),np.min(np.imag(D_roots)))-0.5
        size[3] = max(np.max(np.imag(N_roots)),np.max(np.imag(D_roots)))+0.5
        
    plt.plot([size[0],size[1]],[0,0],'k--')
    plt.plot([0,0],[size[2],size[3]],'r--')
    # Plot labels if multiplicity greater than 1
    x_scale = size[1]-size[0]
    y_scale = size[3]-size[2]
    x_off = 0.03
    y_off = 0.01
    if M > 0:
        #N_roots = np.roots(b)
        N_uniq, N_mult=signal.unique_roots(N_roots,tol=1e-3, rtype='avg')
        plt.plot(np.real(N_uniq),np.imag(N_uniq),'ko',mfc='None',ms=8)
        idx_N_mult = np.nonzero(np.ravel(N_mult>1))[0]
        for k in range(len(idx_N_mult)):
            x_loc = np.real(N_uniq[idx_N_mult[k]]) + x_off*x_scale
            y_loc =np.imag(N_uniq[idx_N_mult[k]]) + y_off*y_scale
            plt.text(x_loc,y_loc,str(N_mult[idx_N_mult[k]]),ha='center',va='bottom',fontsize=10)
    if N > 0:
        #D_roots = np.roots(a)
        D_uniq, D_mult=signal.unique_roots(D_roots,tol=1e-3, rtype='avg')
        plt.plot(np.real(D_uniq),np.imag(D_uniq),'kx',ms=8)
        idx_D_mult = np.nonzero(np.ravel(D_mult>1))[0]
        for k in range(len(idx_D_mult)):
            x_loc = np.real(D_uniq[idx_D_mult[k]]) + x_off*x_scale
            y_loc =np.imag(D_uniq[idx_D_mult[k]]) + y_off*y_scale
            plt.text(x_loc,y_loc,str(D_mult[idx_D_mult[k]]),ha='center',va='bottom',fontsize=10)
    plt.xlabel('Real Part')
    plt.ylabel('Imaginary Part')
    plt.title('Pole-Zero Plot')
    #plt.grid()
    plt.axis(np.array(size))
    return M,N