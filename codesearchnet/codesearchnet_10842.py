def hard_Pk(k,R,SNR,M=2):
    """
    Pk = hard_Pk(k,R,SNR)
    
    Calculates Pk as found in Ziemer & Peterson eq. 7-12, p.505
    
    Mark Wickert and Andrew Smit 2018
    """

    k = int(k)

    if M == 2:
        p = Q_fctn(np.sqrt(2.*R*SNR))
    else:
        p = 4./np.log2(M)*(1 - 1./np.sqrt(M))*\
            Q_fctn(np.sqrt(3*R*np.log2(M)/float(M-1)*SNR))
    Pk = 0
    #if 2*k//2 == k:
    if np.mod(k,2) == 0:
        for e in range(int(k/2+1),int(k+1)):
            Pk += float(factorial(k))/(factorial(e)*factorial(k-e))*p**e*(1-p)**(k-e);
        # Pk += 1./2*float(factorial(k))/(factorial(int(k/2))*factorial(int(k-k/2)))*\
        #       p**(k/2)*(1-p)**(k//2);
        Pk += 1./2*float(factorial(k))/(factorial(int(k/2))*factorial(int(k-k/2)))*\
            p**(k/2)*(1-p)**(k/2);
    elif np.mod(k,2) == 1:
        for e in range(int((k+1)//2),int(k+1)):
            Pk += factorial(k)/(factorial(e)*factorial(k-e))*p**e*(1-p)**(k-e);
    return Pk