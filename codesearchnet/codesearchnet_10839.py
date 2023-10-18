def PLL1(theta,fs,loop_type,Kv,fn,zeta,non_lin):
    """
    Baseband Analog PLL Simulation Model

    :param theta: input phase deviation in radians
    :param fs: sampling rate in sample per second or Hz
    :param loop_type: 1, first-order loop filter F(s)=K_LF; 2, integrator
                with lead compensation F(s) = (1 + s tau2)/(s tau1),
                i.e., a type II, or 3, lowpass with lead compensation
                F(s) = (1 + s tau2)/(1 + s tau1)
    :param Kv: VCO gain in Hz/v; note presently assume Kp = 1v/rad
                and K_LF = 1; the user can easily change this
    :param fn: Loop natural frequency (loops 2 & 3) or cutoff
                frquency (loop 1)
    :param zeta: Damping factor for loops 2 & 3
    :param non_lin: 0, linear phase detector; 1, sinusoidal phase detector
    :return: theta_hat = Output phase estimate of the input theta in radians,
             ev = VCO control voltage,
             phi = phase error = theta - theta_hat

    Notes
    -----
    Alternate input in place of natural frequency, fn, in Hz is
    the noise equivalent bandwidth Bn in Hz.


    Mark Wickert, April 2007 for ECE 5625/4625
    Modified February 2008 and July 2014 for ECE 5675/4675
    Python version August 2014
    """
    T = 1/float(fs)
    Kv = 2*np.pi*Kv # convert Kv in Hz/v to rad/s/v

    if loop_type == 1:
        # First-order loop parameters
        # Note Bn = K/4 Hz but K has units of rad/s
        #fn = 4*Bn/(2*pi);
        K = 2*np.pi*fn # loop natural frequency in rad/s
    elif loop_type == 2:
        # Second-order loop parameters
        #fn = 1/(2*pi) * 2*Bn/(zeta + 1/(4*zeta));
        K = 4 *np.pi*zeta*fn # loop natural frequency in rad/s
        tau2 = zeta/(np.pi*fn)
    elif loop_type == 3:
        # Second-order loop parameters for one-pole lowpass with
        # phase lead correction.
        #fn = 1/(2*pi) * 2*Bn/(zeta + 1/(4*zeta));
        K = Kv # Essentially the VCO gain sets the single-sided
                # hold-in range in Hz, as it is assumed that Kp = 1
                # and KLF = 1.
        tau1 = K/((2*np.pi*fn)**2)
        tau2 = 2*zeta/(2*np.pi*fn)*(1 - 2*np.pi*fn/K*1/(2*zeta))
    else:
        print('Loop type must be 1, 2, or 3')

    # Initialize integration approximation filters
    filt_in_last = 0; filt_out_last = 0;
    vco_in_last = 0; vco_out = 0; vco_out_last = 0;

    # Initialize working and final output vectors
    n = np.arange(len(theta))
    theta_hat = np.zeros_like(theta)
    ev = np.zeros_like(theta)
    phi = np.zeros_like(theta)

    # Begin the simulation loop
    for k in  range(len(n)):
        phi[k] = theta[k] - vco_out
        if non_lin == 1:
            # sinusoidal phase detector
            pd_out = np.sin(phi[k])
        else:
            # Linear phase detector
            pd_out = phi[k]
        # Loop gain
        gain_out = K/Kv*pd_out # apply VCO gain at VCO
        # Loop filter
        if loop_type == 2:
            filt_in = (1/tau2)*gain_out
            filt_out = filt_out_last + T/2*(filt_in + filt_in_last)
            filt_in_last = filt_in
            filt_out_last = filt_out
            filt_out = filt_out + gain_out
        elif loop_type == 3:
            filt_in = (tau2/tau1)*gain_out - (1/tau1)*filt_out_last
            u3 = filt_in + (1/tau2)*filt_out_last
            filt_out = filt_out_last + T/2*(filt_in + filt_in_last)
            filt_in_last = filt_in
            filt_out_last = filt_out
        else:
            filt_out = gain_out;
        # VCO
        vco_in = filt_out
        if loop_type == 3:
            vco_in = u3
        vco_out = vco_out_last + T/2*(vco_in + vco_in_last)
        vco_in_last = vco_in
        vco_out_last = vco_out
        vco_out = Kv*vco_out # apply Kv
        # Measured loop signals
        ev[k] = vco_in
        theta_hat[k] = vco_out
    return theta_hat, ev, phi