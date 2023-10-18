def pid(kp=0., ki=0., kd=0., smooth=0.1):
    r'''Create a callable that implements a PID controller.

    A PID controller returns a control signal :math:`u(t)` given a history of
    error measurements :math:`e(0) \dots e(t)`, using proportional (P), integral
    (I), and derivative (D) terms, according to:

    .. math::

       u(t) = kp * e(t) + ki * \int_{s=0}^t e(s) ds + kd * \frac{de(s)}{ds}(t)

    The proportional term is just the current error, the integral term is the
    sum of all error measurements, and the derivative term is the instantaneous
    derivative of the error measurement.

    Parameters
    ----------
    kp : float
        The weight associated with the proportional term of the PID controller.
    ki : float
        The weight associated with the integral term of the PID controller.
    kd : float
        The weight associated with the derivative term of the PID controller.
    smooth : float in [0, 1]
        Derivative values will be smoothed with this exponential average. A
        value of 1 never incorporates new derivative information, a value of 0.5
        uses the mean of the historic and new information, and a value of 0
        discards historic information (i.e., the derivative in this case will be
        unsmoothed). The default is 0.1.

    Returns
    -------
    controller : callable (float, float) -> float
        Returns a function that accepts an error measurement and a delta-time
        value since the previous measurement, and returns a control signal.
    '''
    state = dict(p=0, i=0, d=0)

    def control(error, dt=1):
        state['d'] = smooth * state['d'] + (1 - smooth) * (error - state['p']) / dt
        state['i'] += error * dt
        state['p'] = error
        return kp * state['p'] + ki * state['i'] + kd * state['d']

    return control