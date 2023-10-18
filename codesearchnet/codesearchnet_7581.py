def arburg(X, order, criteria=None):
    r"""Estimate the complex autoregressive parameters by the Burg algorithm.

    .. math:: x(n) = \sqrt{(v}) e(n) + \sum_{k=1}^{P+1} a(k) x(n-k)

    :param x:  Array of complex data samples (length N)
    :param order: Order of autoregressive process (0<order<N)
    :param criteria: select a criteria to automatically select the order

    :return:
        * A Array of complex autoregressive parameters A(1) to A(order). First
          value (unity) is not included !!
        * P Real variable representing driving noise variance (mean square
          of residual noise) from the whitening operation of the Burg
          filter.
        * reflection coefficients defining the filter of the model.

    .. plot::
        :width: 80%
        :include-source:

        from pylab import plot, log10, linspace, axis
        from spectrum import *

        AR, P, k = arburg(marple_data, 15)
        PSD = arma2psd(AR, sides='centerdc')
        plot(linspace(-0.5, 0.5, len(PSD)), 10*log10(PSD/max(PSD)))
        axis([-0.5,0.5,-60,0])

    .. note::
        1. no detrend. Should remove the mean trend to get PSD. Be careful if
           presence of large mean.
        2. If you don't know what the order value should be, choose the
           criterion='AKICc', which has the least bias and best
           resolution of model-selection criteria.

    .. note:: real and complex results double-checked versus octave using
        complex 64 samples stored in marple_data. It does not agree with Marple
        fortran routine but this is due to the simplex precision of complex
        data in fortran.

    :reference: [Marple]_ [octave]_
    """
    if order <= 0.:
        raise ValueError("order must be > 0")

    if order > len(X):
        raise ValueError("order must be less than length input - 2")

    x = np.array(X)
    N = len(x)

    # Initialisation
    # ------ rho, den
    rho = sum(abs(x)**2.) / float(N)  # Eq 8.21 [Marple]_
    den = rho * 2. * N

    # ---- criteria
    if criteria:
        from spectrum import Criteria
        crit = Criteria(name=criteria, N=N)
        crit.data = rho
        logging.debug('Step {}. old criteria={} new one={}.  rho={}'.format(
                0, crit.old_data, crit.data, rho))

    #p =0
    a = np.zeros(0, dtype=complex)
    ref = np.zeros(0, dtype=complex)
    ef = x.astype(complex)
    eb = x.astype(complex)
    temp = 1.
    #   Main recursion

    for k in range(0, order):

        # calculate the next order reflection coefficient Eq 8.14 Marple
        num = sum([ef[j]*eb[j-1].conjugate() for j in range(k+1, N)])
        den = temp * den - abs(ef[k])**2 - abs(eb[N-1])**2
        kp = -2. * num / den #eq 8.14

        temp = 1. - abs(kp)**2.
        new_rho = temp * rho

        if criteria:
            logging.debug('Step {}. old criteria={} new one={}. rho={}'.format(
                k+1, crit.old_data, crit.data, new_rho))
            #k+1 because order goes from 1 to P whereas k starts at 0.
            status = crit(rho=temp*rho, k=k+1)
            if status is False:
                logging.debug('Stop criteria reached %s %s ' % (crit.data, crit.old_data))
                break
        # this should be after the criteria
        rho = new_rho
        if rho <= 0:
            raise ValueError("Found a negative value (expected positive stricly) %s. Decrease the order" % rho)

        a.resize(a.size+1)
        a[k] = kp
        if k == 0:
            for j in range(N-1, k, -1):
                save2 = ef[j]
                ef[j] = save2 + kp * eb[j-1]          # Eq. (8.7)
                eb[j] = eb[j-1] + kp.conjugate() *  save2

        else:
            # update the AR coeff
            khalf = (k+1)//2  # FIXME here khalf must be an integer
            for j in range(0, khalf):
                ap = a[j] # previous value
                a[j] = ap + kp * a[k-j-1].conjugate()      # Eq. (8.2)
                if j != k-j-1:
                    a[k-j-1] = a[k-j-1] + kp * ap.conjugate()    # Eq. (8.2)

            # update the prediction error
            for j in range(N-1, k, -1):
                save2 = ef[j]
                ef[j] = save2 + kp * eb[j-1]          # Eq. (8.7)
                eb[j] = eb[j-1] + kp.conjugate() *  save2

        # save the reflection coefficient
        ref.resize(ref.size+1)
        ref[k] = kp

    return a, rho, ref