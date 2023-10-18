def toeplitz_multiplication(a,b,v):
    '''
    Multiply Toeplitz matrix with first row a and first column b with vector v
    
    Normal matrix multiplication would require storage and runtime O(n^2);
    embedding into a circulant matrix and using FFT yields O(log(n)n)
    '''
    a = np.reshape(a,(-1))
    b = np.reshape(b,(-1))
    n = len(a)
    c = np.concatenate((a[[0]],b[1:],np.zeros(1),a[-1:0:-1]))
    p = ifft(fft(c)*fft(v.T,n=2*n)).T#fft autopads input with zeros if n is supplied
    if np.all(np.isreal(a)) and np.all(np.isreal(b)) and np.all(np.isreal(v)):
        return np.real(p[:n])
    else:
        return p[:n]