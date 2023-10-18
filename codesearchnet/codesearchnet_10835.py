def NDA_symb_sync(z,Ns,L,BnTs,zeta=0.707,I_ord=3):
    """
    zz,e_tau = NDA_symb_sync(z,Ns,L,BnTs,zeta=0.707,I_ord=3)

           z = complex baseband input signal at nominally Ns samples
               per symbol
          Ns = Nominal number of samples per symbol (Ts/T) in the symbol 
               tracking loop, often 4
        BnTs = time bandwidth product of loop bandwidth and the symbol period,
               thus the loop bandwidth as a fraction of the symbol rate.
        zeta = loop damping factor
       I_ord = interpolator order, 1, 2, or 3
    
       e_tau = the timing error e(k) input to the loop filter

          Kp = The phase detector gain in the symbol tracking loop; for the
               NDA algoithm used here always 1
    
    Mark Wickert July 2014

    Motivated by code found in M. Rice, Digital Communications A Discrete-Time 
    Approach, Prentice Hall, New Jersey, 2009. (ISBN 978-0-13-030497-1).
    """
    # Loop filter parameters
    K0 = -1.0 # The modulo 1 counter counts down so a sign change in loop
    Kp = 1.0
    K1 = 4*zeta/(zeta + 1/(4*zeta))*BnTs/Ns/Kp/K0
    K2 = 4/(zeta + 1/(4*zeta))**2*(BnTs/Ns)**2/Kp/K0
    zz = np.zeros(len(z),dtype=np.complex128)
    #zz = np.zeros(int(np.floor(len(z)/float(Ns))),dtype=np.complex128)
    e_tau = np.zeros(len(z))
    #e_tau = np.zeros(int(np.floor(len(z)/float(Ns))))
    #z_TED_buff = np.zeros(Ns)
    c1_buff = np.zeros(2*L+1)

    vi = 0
    CNT_next = 0
    mu_next = 0
    underflow = 0
    epsilon = 0
    mm = 1
    z = np.hstack(([0], z))
    for nn in range(1,Ns*int(np.floor(len(z)/float(Ns)-(Ns-1)))):
        # Define variables used in linear interpolator control
        CNT = CNT_next
        mu = mu_next
        if underflow == 1:
            if I_ord == 1:
                # Decimated interpolator output (piecewise linear)
                z_interp = mu*z[nn] + (1 - mu)*z[nn-1]
            elif I_ord == 2:
                # Decimated interpolator output (piecewise parabolic)
                # in Farrow form with alpha = 1/2
                v2 = 1/2.*np.sum(z[nn+2:nn-1-1:-1]*[1, -1, -1, 1])
                v1 = 1/2.*np.sum(z[nn+2:nn-1-1:-1]*[-1, 3, -1, -1])
                v0 = z[nn]
                z_interp = (mu*v2 + v1)*mu + v0
            elif I_ord == 3:
                # Decimated interpolator output (piecewise cubic)
                # in Farrow form
                v3 = np.sum(z[nn+2:nn-1-1:-1]*[1/6., -1/2., 1/2., -1/6.])
                v2 = np.sum(z[nn+2:nn-1-1:-1]*[0, 1/2., -1, 1/2.])
                v1 = np.sum(z[nn+2:nn-1-1:-1]*[-1/6., 1, -1/2., -1/3.])
                v0 = z[nn]
                z_interp = ((mu*v3 + v2)*mu + v1)*mu + v0
            else:
                print('Error: I_ord must 1, 2, or 3')
            # Form TED output that is smoothed using 2*L+1 samples
            # We need Ns interpolants for this TED: 0:Ns-1
            c1 = 0
            for kk in range(Ns):
                if I_ord == 1:
                    # piecewise linear interp over Ns samples for TED
                    z_TED_interp = mu*z[nn+kk] + (1 - mu)*z[nn-1+kk]
                elif I_ord == 2:
                    # piecewise parabolic in Farrow form with alpha = 1/2
                    v2 = 1/2.*np.sum(z[nn+kk+2:nn+kk-1-1:-1]*[1, -1, -1, 1])
                    v1 = 1/2.*np.sum(z[nn+kk+2:nn+kk-1-1:-1]*[-1, 3, -1, -1])
                    v0 = z[nn+kk]
                    z_TED_interp = (mu*v2 + v1)*mu + v0
                elif I_ord == 3:
                    # piecewise cubic in Farrow form
                    v3 = np.sum(z[nn+kk+2:nn+kk-1-1:-1]*[1/6., -1/2., 1/2., -1/6.])
                    v2 = np.sum(z[nn+kk+2:nn+kk-1-1:-1]*[0, 1/2., -1, 1/2.])
                    v1 = np.sum(z[nn+kk+2:nn+kk-1-1:-1]*[-1/6., 1, -1/2., -1/3.])
                    v0 = z[nn+kk]
                    z_TED_interp = ((mu*v3 + v2)*mu + v1)*mu + v0
                else:
                    print('Error: I_ord must 1, 2, or 3')
                c1 = c1 + np.abs(z_TED_interp)**2 * np.exp(-1j*2*np.pi/Ns*kk)
            c1 = c1/Ns
            # Update 2*L+1 length buffer for TED output smoothing
            c1_buff = np.hstack(([c1], c1_buff[:-1]))
            # Form the smoothed TED output
            epsilon = -1/(2*np.pi)*np.angle(np.sum(c1_buff)/(2*L+1))
            # Save symbol spaced (decimated to symbol rate) interpolants in zz
            zz[mm] = z_interp
            e_tau[mm] = epsilon # log the error to the output vector e
            mm += 1
        else:
            # Simple zezo-order hold interpolation between symbol samples
            # we just coast using the old value
            #epsilon = 0
            pass
        vp = K1*epsilon       # proportional component of loop filter
        vi = vi + K2*epsilon  # integrator component of loop filter
        v = vp + vi           # loop filter output
        W = 1/float(Ns) + v          # counter control word
       
        # update registers
        CNT_next = CNT - W           # Update counter value for next cycle
        if CNT_next < 0:             # Test to see if underflow has occured
            CNT_next = 1 + CNT_next  # Reduce counter value modulo-1 if underflow
            underflow = 1            # Set the underflow flag
            mu_next = CNT/W          # update mu
        else:
            underflow = 0
            mu_next = mu
    # Remove zero samples at end
    zz = zz[:-(len(zz)-mm+1)]
    # Normalize so symbol values have a unity magnitude
    zz /=np.std(zz)
    e_tau = e_tau[:-(len(e_tau)-mm+1)]
    return zz, e_tau