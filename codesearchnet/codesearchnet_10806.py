def complex2wav(filename,rate,x):
    """
    Save a complex signal vector to a wav file for compact binary
    storage of 16-bit signal samples. The wav left and right channels
    are used to save real (I) and imaginary (Q) values. The rate is
    just a convent way of documenting the original signal sample rate.

    complex2wav(filename,rate,x)

    Mark Wickert April 2014
    """
    x_wav = np.hstack((np.array([x.real]).T,np.array([x.imag]).T))
    ss.to_wav(filename, rate, x_wav)
    print('Saved as binary wav file with (I,Q)<=>(L,R)')