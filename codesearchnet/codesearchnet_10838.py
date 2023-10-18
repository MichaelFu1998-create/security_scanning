def phase_step(z,Ns,p_step,Nstep):
    """
    Create a one sample per symbol signal containing a phase rotation
    step Nsymb into the waveform.

    :param z: complex baseband signal after matched filter
    :param Ns: number of sample per symbol
    :param p_step: size in radians of the phase step
    :param Nstep: symbol sample location where the step turns on
    :return: the one sample symbol signal containing the phase step

    Mark Wickert July 2014
    """
    nn = np.arange(0,len(z[::Ns]))
    theta = np.zeros(len(nn))
    idx = np.where(nn >= Nstep)
    theta[idx] = p_step*np.ones(len(idx))
    z_rot = z[::Ns]*np.exp(1j*theta)
    return z_rot