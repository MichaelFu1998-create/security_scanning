def time_delay(x,D,N=4):
    """
    A time varying time delay which takes advantage of the Farrow structure
    for cubic interpolation:

    y = time_delay(x,D,N = 3)

    Note that D is an array of the same length as the input signal x. This
    allows you to make the delay a function of time. If you want a constant 
    delay just use D*zeros(len(x)). The minimum delay allowable is one sample
    or D = 1.0. This is due to the causal system nature of the Farrow 
    structure.

    A founding paper on the subject of interpolators is: C. W. Farrow, "A
    Continuously variable Digital Delay Element," Proceedings of the IEEE
    Intern. Symp. on Circuits Syst., pp. 2641-2645, June 1988.

    Mark Wickert, February 2014
    """

    if type(D) == float or type(D) == int:
        #Make sure D stays with in the tapped delay line bounds
        if int(np.fix(D)) < 1:
            print('D has integer part less than one')
            exit(1)
        if int(np.fix(D)) > N-2:
            print('D has integer part greater than N - 2')
            exit(1)
        # Filter 4-tap input with four Farrow FIR filters
        # Since the time delay is a constant, the LTI filter
        # function from scipy.signal is convenient.
        D_frac = D - np.fix(D)
        Nd = int(np.fix(D))
        b = np.zeros(Nd + 4)
        # Load Lagrange coefficients into the last four FIR taps
        b[Nd] = -(D_frac-1)*(D_frac-2)*(D_frac-3)/6.
        b[Nd + 1] = D_frac*(D_frac-2)*(D_frac-3)/2.
        b[Nd + 2] = -D_frac*(D_frac-1)*(D_frac-3)/2.
        b[Nd + 3] = D_frac*(D_frac-1)*(D_frac-2)/6.
        # Do all of the filtering in one step for this special case
        # of a fixed delay.
        y = signal.lfilter(b,[1],x)
    else:
        # Make sure D stays with in the tapped delay line bounds
        if np.fix(np.min(D)) < 1:
            print('D has integer part less than one')
            exit(1)
        if np.fix(np.max(D)) > N-2:
            print('D has integer part greater than N - 2')
            exit(1)
        y = np.zeros(len(x))
        X = np.zeros(N+1)
        # Farrow filter tap weights
        W3 = np.array([[1./6, -1./2, 1./2, -1./6]])
        W2 = np.array([[0, 1./2, -1., 1./2]])
        W1 = np.array([[-1./6, 1., -1./2, -1./3]])
        W0 = np.array([[0, 0, 1., 0]])
        for k in range(len(x)):
            Nd = int(np.fix(D[k]))
            mu = 1 - (D[k]-np.fix(D[k]))
            # Form a row vector of signal samples, present and past values
            X = np.hstack((np.array(x[k]), X[:-1]))
            # Filter 4-tap input with four Farrow FIR filters
            # Here numpy dot(A,B) performs the matrix multiply
            # since the filter has time-varying coefficients
            v3 = np.dot(W3,np.array(X[Nd-1:Nd+3]).T)
            v2 = np.dot(W2,np.array(X[Nd-1:Nd+3]).T)
            v1 = np.dot(W1,np.array(X[Nd-1:Nd+3]).T)
            v0 = np.dot(W0,np.array(X[Nd-1:Nd+3]).T)
            #Combine sub-filter outputs using mu = 1 - d
            y[k] = ((v3[0]*mu + v2[0])*mu + v1[0])*mu + v0[0]
    return y