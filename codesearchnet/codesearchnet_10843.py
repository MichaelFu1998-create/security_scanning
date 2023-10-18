def soft_Pk(k,R,SNR,M=2):
    """
    Pk = soft_Pk(k,R,SNR)
    
    Calculates Pk as found in Ziemer & Peterson eq. 7-13, p.505
    
    Mark Wickert November 2014
    """
    if M == 2:
        Pk = Q_fctn(np.sqrt(2.*k*R*SNR))
    else:
        Pk = 4./np.log2(M)*(1 - 1./np.sqrt(M))*\
             Q_fctn(np.sqrt(3*k*R*np.log2(M)/float(M-1)*SNR))
    
    return Pk