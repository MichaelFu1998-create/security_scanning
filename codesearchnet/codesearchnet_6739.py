def Antoine(T, A, B, C, base=10.0):
    r'''Calculates vapor pressure of a chemical using the Antoine equation.
    Parameters `A`, `B`, and `C` are chemical-dependent. Parameters can be 
    found in numerous sources; however units of the coefficients used vary.
    Originally proposed by Antoine (1888) [2]_.

    .. math::
        \log_{\text{base}} P^{\text{sat}} = A - \frac{B}{T+C}

    Parameters
    ----------
    T : float
        Temperature of fluid, [K]
    A, B, C : floats
        Regressed coefficients for Antoine equation for a chemical

    Returns
    -------
    Psat : float
        Vapor pressure calculated with coefficients [Pa]
    
    Other Parameters
    ----------------
    Base : float
        Optional base of logarithm; 10 by default

    Notes
    -----
    Assumes coefficients are for calculating vapor pressure in Pascal. 
    Coefficients should be consistent with input temperatures in Kelvin;
    however, if both the given temperature and units are specific to degrees
    Celcius, the result will still be correct.
    
    **Converting units in input coefficients:**
    
        * **ln to log10**: Divide A and B by ln(10)=2.302585 to change  
          parameters for a ln equation to a log10 equation.
        * **log10 to ln**: Multiply A and B by ln(10)=2.302585 to change 
          parameters for a log equation to a ln equation.
        * **mmHg to Pa**: Add log10(101325/760)= 2.1249 to A.
        * **kPa to Pa**: Add log_{base}(1000)= 6.908 to A for log(base)
        * **°C to K**: Subtract 273.15 from C only!

    Examples
    --------
    Methane, coefficients from [1]_, at 100 K:
    
    >>> Antoine(100.0, 8.7687, 395.744, -6.469)
    34478.367349639906
    
    Tetrafluoromethane, coefficients from [1]_, at 180 K
    
    >>> Antoine(180, A=8.95894, B=510.595, C=-15.95)
    702271.0518579542
    
    Oxygen at 94.91 K, with coefficients from [3]_ in units of °C, mmHg, log10,
    showing the conversion of coefficients A (mmHg to Pa) and C (°C to K)
    
    >>> Antoine(94.91, 6.83706+2.1249, 339.2095, 268.70-273.15)
    162978.88655572367

    References
    ----------
    .. [1] Poling, Bruce E. The Properties of Gases and Liquids. 5th edition.
       New York: McGraw-Hill Professional, 2000.
    .. [2] Antoine, C. 1888. Tensions des Vapeurs: Nouvelle Relation Entre les 
       Tensions et les Tempé. Compt.Rend. 107:681-684.
    .. [3] Yaws, Carl L. The Yaws Handbook of Vapor Pressure: Antoine 
       Coefficients. 1 edition. Houston, Tex: Gulf Publishing Company, 2007.
    '''
    return base**(A-B/(T+C))