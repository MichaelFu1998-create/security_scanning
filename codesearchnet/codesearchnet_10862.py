def ser2ber(q,n,d,t,ps):
    """
    Converts symbol error rate to bit error rate. Taken from Ziemer and
    Tranter page 650. Necessary when comparing different types of block codes.
    
    parameters
    ----------  
    q: size of the code alphabet for given modulation type (BPSK=2)
    n: number of channel bits
    d: distance (2e+1) where e is the number of correctable errors per code word.
       For hamming codes, e=1, so d=3.
    t: number of correctable errors per code word
    ps: symbol error probability vector
    
    returns
    -------
    ber: bit error rate
    
    """
    lnps = len(ps) # len of error vector
    ber = np.zeros(lnps) # inialize output vector
    for k in range(0,lnps): # iterate error vector
        ser = ps[k] # channel symbol error rate
        sum1 = 0 # initialize sums
        sum2 = 0
        for i in range(t+1,d+1):
            term = special.comb(n,i)*(ser**i)*((1-ser))**(n-i)
            sum1 = sum1 + term
        for i in range(d+1,n+1):
            term = (i)*special.comb(n,i)*(ser**i)*((1-ser)**(n-i))
            sum2 = sum2+term
        ber[k] = (q/(2*(q-1)))*((d/n)*sum1+(1/n)*sum2)
    
    return ber