def _log_likelihood_transit_plus_line(theta, params, model, t, data_flux,
                                      err_flux, priorbounds):
    '''
    Given a batman TransitModel and its proposed parameters (theta), update the
    batman params object with the proposed parameters and evaluate the gaussian
    likelihood.

    Note: the priorbounds are only needed to parse theta.
    '''

    u = []
    for ix, key in enumerate(sorted(priorbounds.keys())):

        if key == 'rp':
            params.rp = theta[ix]
        elif key == 't0':
            params.t0 = theta[ix]
        elif key == 'sma':
            params.a = theta[ix]
        elif key == 'incl':
            params.inc = theta[ix]
        elif key == 'period':
            params.per = theta[ix]
        elif key == 'ecc':
            params.per = theta[ix]
        elif key == 'omega':
            params.w = theta[ix]
        elif key == 'u_linear':
            u.append(theta[ix])
        elif key == 'u_quadratic':
            u.append(theta[ix])
            params.u = u
        elif key == 'poly_order0':
            poly_order0 = theta[ix]
        elif key == 'poly_order1':
            poly_order1 = theta[ix]

    try:
        poly_order0
    except Exception as e:
        poly_order0 = 0
    else:
        pass

    transit = model.light_curve(params)
    line = poly_order0 + t*poly_order1
    model = transit + line

    residuals = data_flux - model

    log_likelihood = -0.5*(
        np.sum((residuals/err_flux)**2 + np.log(2*np.pi*(err_flux)**2))
    )

    return log_likelihood