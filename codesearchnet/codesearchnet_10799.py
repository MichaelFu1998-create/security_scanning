def sinusoidAWGN(x,SNRdB):
    """
    Add white Gaussian noise to a single real sinusoid.
    
    Input a single sinusoid to this function and it returns a noisy
    sinusoid at a specific SNR value in dB. Sinusoid power is calculated
    using np.var.
    
    Parameters
    ----------
    x : Input signal as ndarray consisting of a single sinusoid
    SNRdB : SNR in dB for output sinusoid
         
    Returns
    -------
    y : Noisy sinusoid return vector

    Examples
    --------
    >>> # set the SNR to 10 dB
    >>> n = arange(0,10000)
    >>> x = cos(2*pi*0.04*n)
    >>> y = sinusoidAWGN(x,10.0)
    """
    # Estimate signal power
    x_pwr = np.var(x)

    # Create noise vector
    noise = np.sqrt(x_pwr/10**(SNRdB/10.))*np.random.randn(len(x));
    return x + noise