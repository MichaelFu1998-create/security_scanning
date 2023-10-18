def _arburg2(X, order):
    """This version is 10 times faster than arburg, but the output rho is not correct.


    returns [1 a0,a1, an-1]

    """
    x = np.array(X)
    N = len(x)

    if order <= 0.:
        raise ValueError("order must be > 0")

    # Initialisation
    # ------ rho, den
    rho = sum(abs(x)**2.) / N  # Eq 8.21 [Marple]_
    den = rho * 2. * N

    # ------ backward and forward errors
    ef = np.zeros(N, dtype=complex)
    eb = np.zeros(N, dtype=complex)
    for j in range(0, N):  #eq 8.11
        ef[j] = x[j]
        eb[j] = x[j]

    # AR order to be stored
    a = np.zeros(1, dtype=complex)
    a[0] = 1
    # ---- rflection coeff to be stored
    ref = np.zeros(order, dtype=complex)

    temp = 1.
    E = np.zeros(order+1)
    E[0] = rho

    for m in range(0, order):
        #print m
        # Calculate the next order reflection (parcor) coefficient
        efp = ef[1:]
        ebp = eb[0:-1]
        #print efp, ebp
        num = -2.* np.dot(ebp.conj().transpose(),  efp)
        den = np.dot(efp.conj().transpose(),  efp)
        den += np.dot(ebp,  ebp.conj().transpose())
        ref[m] = num / den

        # Update the forward and backward prediction errors
        ef = efp + ref[m] * ebp
        eb = ebp + ref[m].conj().transpose() * efp

        # Update the AR coeff.
        a.resize(len(a)+1)
        a = a + ref[m] * np.flipud(a).conjugate()

        # Update the prediction error
        E[m+1] = (1 - ref[m].conj().transpose()*ref[m]) * E[m]
        #print 'REF', ref, num, den
    return a, E[-1], ref