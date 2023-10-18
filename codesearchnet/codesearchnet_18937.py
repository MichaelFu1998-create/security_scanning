def SIRode(y0, time, beta, gamma):
    """Integrate SIR epidemic model

    Simulate a very basic deterministic SIR system.

    :param 2x1 numpy array y0: initial conditions
    :param Ntimestep length numpy array time: Vector of time points that \
    solution is returned at
    :param float beta: transmission rate
    :param float gamma: recovery rate

    :returns: (2)x(Ntimestep) numpy array Xsim: first row S(t), second row I(t)
    
    """
    
    Xsim = rk4(SIR_D, y0, time, args=(beta,gamma,))
    Xsim = Xsim.transpose()
    return Xsim