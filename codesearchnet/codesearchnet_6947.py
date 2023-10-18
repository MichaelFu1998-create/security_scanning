def viscosity_converter(val, old_scale, new_scale, extrapolate=False):
    r'''Converts kinematic viscosity values from different scales which have
    historically been used. Though they may not be in use much, some standards
    still specify values in these scales.

    Parameters
    ----------
    val : float
        Viscosity value in the specified scale; [m^2/s] if 
        'kinematic viscosity'; [degrees] if Engler or Barbey; [s] for the other
        scales.
    old_scale : str
        String representing the scale that `val` is in originally.
    new_scale : str
        String representing the scale that `val` should be converted to.
    extrapolate : bool
        If True, a conversion will be performed even if outside the limits of
        either scale; if False, and either value is outside a limit, an
        exception will be raised.
        
    Returns
    -------
    result : float
        Viscosity value in the specified scale; [m^2/s] if 
        'kinematic viscosity'; [degrees] if Engler or Barbey; [s] for the other
        scales

    Notes
    -----
    The valid scales for this function are any of the following:
        
    ['a&w b', 'a&w crucible', 'american can', 'astm 0.07', 'astm 0.10', 
    'astm 0.15', 'astm 0.20', 'astm 0.25', 'barbey', 'caspers tin plate', 
    'continental can', 'crown cork and seal', 'demmier #1', 'demmier #10', 
    'engler', 'ford cup #3', 'ford cup #4', 'kinematic viscosity', 
    'mac michael', 'murphy varnish', 'parlin cup #10', 'parlin cup #15', 
    'parlin cup #20', 'parlin cup #25', 'parlin cup #30', 'parlin cup #7', 
    'pratt lambert a', 'pratt lambert b', 'pratt lambert c', 'pratt lambert d', 
    'pratt lambert e', 'pratt lambert f', 'pratt lambert g', 'pratt lambert h',
    'pratt lambert i', 'redwood admiralty', 'redwood standard', 
    'saybolt furol', 'saybolt universal', 'scott', 'stormer 100g load', 
    'westinghouse', 'zahn cup #1', 'zahn cup #2', 'zahn cup #3', 'zahn cup #4',
    'zahn cup #5']
    
    Some of those scales are converted linearly; the rest use tabulated data
    and splines.

    Because the conversion is performed by spline functions, a re-conversion
    of a value will not yield exactly the original value. However, it is quite
    close.
    
    The method 'Saybolt universal' has a special formula implemented for its
    conversion, from [4]_. It is designed for maximum backwards compatibility
    with prior experimental data. It is solved by newton's method when 
    kinematic viscosity is desired as an output.
    
    .. math::
        SUS_{eq} = 4.6324\nu_t + \frac{[1.0 + 0.03264\nu_t]}
        {[(3930.2 + 262.7\nu_t + 23.97\nu_t^2 + 1.646\nu_t^3)\times10^{-5})]}

    Examples
    --------
    >>> viscosity_converter(8.79, 'engler', 'parlin cup #7')
    52.5
    >>> viscosity_converter(700, 'Saybolt Universal Seconds', 'kinematic viscosity')
    0.00015108914751515542

    References
    ----------
    .. [1] Hydraulic Institute. Hydraulic Institute Engineering Data Book. 
       Cleveland, Ohio: Hydraulic Institute, 1990.
    .. [2] Gardner/Sward. Paint Testing Manual. Physical and Chemical 
       Examination of Paints, Varnishes, Lacquers, and Colors. 13th Edition. 
       ASTM, 1972.
    .. [3] Euverard, M. R., The Efflux Type Viscosity Cup. National Paint, 
       Varnish, and Lacquer Association, 1948.
    .. [4] API Technical Data Book: General Properties & Characterization.
       American Petroleum Institute, 7E, 2005.
    .. [5] ASTM. Standard Practice for Conversion of Kinematic Viscosity to 
       Saybolt Universal Viscosity or to Saybolt Furol Viscosity. D 2161 - 93.
    '''

    def range_check(visc, scale):
        scale_min, scale_max, nu_min, nu_max = viscosity_converter_limits[scale]
        
        if visc < scale_min*(1.-1E-7) or visc > scale_max*(1.+1E-7):
            raise Exception('Viscosity conversion is outside the limits of the '
                            '%s scale; given value is %s, but the range of the '
                            'scale is from %s to %s. Set `extrapolate` to True '
                            'to perform the conversion anyway.' %(scale, visc, scale_min, scale_max))

    def range_check_linear(val, c, tmin, scale):
        if val < tmin:
            raise Exception('Viscosity conversion is outside the limits of the '
                            '%s scale; given value is %s, but the minimum time '
                            'for this scale is %s s. Set `extrapolate` to True '
                            'to perform the conversion anyway.' %(scale, val, tmin))

    old_scale = old_scale.lower().replace('degrees', '').replace('seconds', '').strip()
    new_scale = new_scale.lower().replace('degrees', '').replace('seconds', '').strip()
    
    def Saybolt_universal_eq(nu):
        return (4.6324*nu + (1E5 + 3264.*nu)/(nu*(nu*(1.646*nu + 23.97) 
                                              + 262.7) + 3930.2))

    # Convert to kinematic viscosity
    if old_scale == 'kinematic viscosity':
        val = 1E6*val # convert to centistokes, the basis of the functions
    elif old_scale == 'saybolt universal':
        if not extrapolate:
            range_check(val, old_scale)
        to_solve = lambda nu: Saybolt_universal_eq(nu) - val
        val = newton(to_solve, 1)
    elif old_scale in viscosity_converters_to_nu:
        if not extrapolate:
            range_check(val, old_scale)
        val = exp(viscosity_converters_to_nu[old_scale](log(val)))
    elif old_scale in viscosity_scales_linear:
        c, tmin = viscosity_scales_linear[old_scale]
        if not extrapolate:
            range_check_linear(val, c, tmin, old_scale)
        val = c*val # convert from seconds to centistokes
    else:
        keys = sorted(set(list(viscosity_scales.keys()) + list(viscosity_scales_linear.keys())))
        raise Exception('Scale "%s" not recognized - allowable values are any of %s.' %(old_scale, keys))

    # Convert to desired scale
    if new_scale == 'kinematic viscosity':
        val = 1E-6*val # convert to m^2/s
    elif new_scale == 'saybolt universal':
        val = Saybolt_universal_eq(val)
    elif new_scale in viscosity_converters_from_nu:
        val = exp(viscosity_converters_from_nu[new_scale](log(val)))
        if not extrapolate:
            range_check(val, new_scale)
    elif new_scale in viscosity_scales_linear:
        c, tmin = viscosity_scales_linear[new_scale]
        val = val/c # convert from centistokes to seconds
        if not extrapolate:
            range_check_linear(val, c, tmin, new_scale)
    else:
        keys = sorted(set(list(viscosity_scales.keys()) + list(viscosity_scales_linear.keys())))
        raise Exception('Scale "%s" not recognized - allowable values are any of %s.' %(new_scale, keys))
    return float(val)