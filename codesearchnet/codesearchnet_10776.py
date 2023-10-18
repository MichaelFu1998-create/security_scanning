def freqz_cas(sos,w):
    """
    Cascade frequency response
    
    Mark Wickert October 2016
    """
    Ns,Mcol = sos.shape
    w,Hcas = signal.freqz(sos[0,:3],sos[0,3:],w)
    for k in range(1,Ns):
        w,Htemp = signal.freqz(sos[k,:3],sos[k,3:],w)
        Hcas *= Htemp
    return w, Hcas