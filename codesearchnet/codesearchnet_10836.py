def DD_carrier_sync(z,M,BnTs,zeta=0.707,type=0):
    """
    z_prime,a_hat,e_phi = DD_carrier_sync(z,M,BnTs,zeta=0.707,type=0)
    Decision directed carrier phase tracking
    
           z = complex baseband PSK signal at one sample per symbol
           M = The PSK modulation order, i.e., 2, 8, or 8.
        BnTs = time bandwidth product of loop bandwidth and the symbol period,
               thus the loop bandwidth as a fraction of the symbol rate.
        zeta = loop damping factor
        type = Phase error detector type: 0 <> ML, 1 <> heuristic
    
     z_prime = phase rotation output (like soft symbol values)
       a_hat = the hard decision symbol values landing at the constellation
               values
       e_phi = the phase error e(k) into the loop filter

          Ns = Nominal number of samples per symbol (Ts/T) in the carrier 
               phase tracking loop, almost always 1
          Kp = The phase detector gain in the carrier phase tracking loop; 
               This value depends upon the algorithm type. For the ML scheme
               described at the end of notes Chapter 9, A = 1, K 1/sqrt(2),
               so Kp = sqrt(2).
    
    Mark Wickert July 2014

    Motivated by code found in M. Rice, Digital Communications A Discrete-Time 
    Approach, Prentice Hall, New Jersey, 2009. (ISBN 978-0-13-030497-1).
    """
    Ns = 1
    Kp = np.sqrt(2.) # for type 0
    z_prime = np.zeros_like(z)
    a_hat = np.zeros_like(z)
    e_phi = np.zeros(len(z))
    theta_h = np.zeros(len(z))
    theta_hat = 0

    # Tracking loop constants
    K0 = 1;
    K1 = 4*zeta/(zeta + 1/(4*zeta))*BnTs/Ns/Kp/K0;
    K2 = 4/(zeta + 1/(4*zeta))**2*(BnTs/Ns)**2/Kp/K0;
    
    # Initial condition
    vi = 0
    for nn in range(len(z)):
        # Multiply by the phase estimate exp(-j*theta_hat[n])
        z_prime[nn] = z[nn]*np.exp(-1j*theta_hat)
        if M == 2:
            a_hat[nn] = np.sign(z_prime[nn].real) + 1j*0
        elif M == 4:
            a_hat[nn] = np.sign(z_prime[nn].real) + 1j*np.sign(z_prime[nn].imag)
        elif M == 8:
            a_hat[nn] = np.angle(z_prime[nn])/(2*np.pi/8.)
            # round to the nearest integer and fold to nonnegative
            # integers; detection into M-levels with thresholds at mid points.
            a_hat[nn] = np.mod(round(a_hat[nn]),8)
            a_hat[nn] = np.exp(1j*2*np.pi*a_hat[nn]/8)
        else:
           raise ValueError('M must be 2, 4, or 8')
        if type == 0:
            # Maximum likelihood (ML)
            e_phi[nn] = z_prime[nn].imag * a_hat[nn].real - \
                    z_prime[nn].real * a_hat[nn].imag
        elif type == 1:
            # Heuristic
            e_phi[nn] = np.angle(z_prime[nn]) - np.angle(a_hat[nn])
        else:
            raise ValueError('Type must be 0 or 1')
        vp = K1*e_phi[nn]      # proportional component of loop filter
        vi = vi + K2*e_phi[nn] # integrator component of loop filter
        v = vp + vi        # loop filter output
        theta_hat = np.mod(theta_hat + v,2*np.pi)
        theta_h[nn] = theta_hat # phase track output array
        #theta_hat = 0 # for open-loop testing
    
    # Normalize outputs to have QPSK points at (+/-)1 + j(+/-)1
    #if M == 4:
    #    z_prime = z_prime*np.sqrt(2)
    return z_prime, a_hat, e_phi, theta_h