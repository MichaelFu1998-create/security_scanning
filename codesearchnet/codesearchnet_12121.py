def log_posterior_transit_plus_line(theta, params, model, t, flux, err_flux,
                                    priorbounds):
    '''
    Evaluate posterior probability given proposed model parameters and
    the observed flux timeseries.
    '''
    lp = _log_prior_transit_plus_line(theta, priorbounds)
    if not np.isfinite(lp):
        return -np.inf
    else:
        return (
            lp + _log_likelihood_transit_plus_line(
                theta, params, model, t, flux, err_flux, priorbounds)
        )