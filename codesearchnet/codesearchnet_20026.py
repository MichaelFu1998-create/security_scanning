def convolve(signal,kernel):
    """
    This applies a kernel to a signal through convolution and returns the result.

    Some magic is done at the edges so the result doesn't apprach zero:
        1. extend the signal's edges with len(kernel)/2 duplicated values
        2. perform the convolution ('same' mode)
        3. slice-off the ends we added
        4. return the same number of points as the original
    """
    pad=np.ones(len(kernel)/2)
    signal=np.concatenate((pad*signal[0],signal,pad*signal[-1]))
    signal=np.convolve(signal,kernel,mode='same')
    signal=signal[len(pad):-len(pad)]
    return signal