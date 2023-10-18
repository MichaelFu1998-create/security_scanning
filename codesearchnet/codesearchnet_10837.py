def time_step(z,Ns,t_step,Nstep):
    """
    Create a one sample per symbol signal containing a phase rotation
    step Nsymb into the waveform.

    :param z: complex baseband signal after matched filter
    :param Ns: number of sample per symbol
    :param t_step: in samples relative to Ns
    :param Nstep: symbol sample location where the step turns on
    :return: the one sample per symbol signal containing the phase step

    Mark Wickert July 2014
    """
    z_step = np.hstack((z[:Ns*Nstep], z[(Ns*Nstep+t_step):], np.zeros(t_step)))
    return z_step