def xcorr(x1,x2,Nlags):
    """
    r12, k = xcorr(x1,x2,Nlags), r12 and k are ndarray's
    Compute the energy normalized cross correlation between the sequences
    x1 and x2. If x1 = x2 the cross correlation is the autocorrelation.
    The number of lags sets how many lags to return centered about zero
    """
    K = 2*(int(np.floor(len(x1)/2)))
    X1 = fft.fft(x1[:K])
    X2 = fft.fft(x2[:K])
    E1 = sum(abs(x1[:K])**2)
    E2 = sum(abs(x2[:K])**2)
    r12 = np.fft.ifft(X1*np.conj(X2))/np.sqrt(E1*E2)
    k = np.arange(K) - int(np.floor(K/2))
    r12 = np.fft.fftshift(r12)
    idx = np.nonzero(np.ravel(abs(k) <= Nlags))
    return r12[idx], k[idx]