def cruise_control(wn,zeta,T,vcruise,vmax,tf_mode='H'):
    """
    Cruise control with PI controller and hill disturbance.

    This function returns various system function configurations
    for a the cruise control Case Study example found in 
    the supplementary article. The plant model is obtained by the
    linearizing the equations of motion and the controller contains a
    proportional and integral gain term set via the closed-loop parameters
    natuarl frequency wn (rad/s) and damping zeta.

    Parameters
    ----------
    wn : closed-loop natural frequency in rad/s, nominally 0.1
    zeta : closed-loop damping factor, nominally 1.0
    T : vehicle time constant, nominally 10 s
    vcruise : cruise velocity set point, nominally 75 mph
    vmax : maximum vehicle velocity, nominally 120 mph
    tf_mode : 'H', 'HE', 'HVW', or 'HED' controls the system function returned by the function 
    'H'   : closed-loop system function V(s)/R(s)
    'HE'  : closed-loop system function E(s)/R(s)
    'HVW' : closed-loop system function V(s)/W(s)
    'HED' : closed-loop system function E(s)/D(s), where D is the hill disturbance input

    Returns
    -------
    b : numerator coefficient ndarray
    a : denominator coefficient ndarray 

    Examples
    --------
    >>> # return the closed-loop system function output/input velocity
    >>> b,a = cruise_control(wn,zeta,T,vcruise,vmax,tf_mode='H')
    >>> # return the closed-loop system function loop error/hill disturbance
    >>> b,a = cruise_control(wn,zeta,T,vcruise,vmax,tf_mode='HED')
    """
    tau = T/2.*vmax/vcruise
    g = 9.8
    g *= 3*60**2/5280. # m/s to mph conversion
    Kp = T*(2*zeta*wn-1/tau)/vmax
    Ki = T*wn**2./vmax
    K = Kp*vmax/T
    print('wn = ', np.sqrt(K/(Kp/Ki)))
    print('zeta = ', (K + 1/tau)/(2*wn))
    a = np.array([1, 2*zeta*wn, wn**2])
    if tf_mode == 'H':
        b = np.array([K, wn**2])      
    elif tf_mode == 'HE':
        b = np.array([1, 2*zeta*wn-K, 0.])   
    elif tf_mode == 'HVW':
        b = np.array([ 1, wn**2/K+1/tau, wn**2/(K*tau)])
        b *= Kp
    elif tf_mode == 'HED':
        b = np.array([g, 0])
    else:
        raise ValueError('tf_mode must be: H, HE, HVU, or HED')
    return b, a