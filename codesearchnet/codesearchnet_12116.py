def _transit_model(times, t0, per, rp, a, inc, ecc, w, u, limb_dark,
                   exp_time_minutes=2, supersample_factor=7):
    '''This returns a BATMAN planetary transit model.

    Parameters
    ----------

    times : np.array
        The times at which the model will be evaluated.

    t0 : float
        The time of periastron for the transit.

    per : float
        The orbital period of the planet.

    rp : float
        The stellar radius of the planet's star (in Rsun).

    a : float
        The semi-major axis of the planet's orbit (in Rsun).

    inc : float
        The orbital inclination (in degrees).

    ecc : float
        The eccentricity of the orbit.

    w : float
        The longitude of periastron (in degrees).

    u : list of floats
        The limb darkening coefficients specific to the limb darkening model
        used.

    limb_dark : {"uniform", "linear", "quadratic", "square-root", "logarithmic", "exponential", "power2", "custom"}
        The type of limb darkening model to use. See the full list here:

        https://www.cfa.harvard.edu/~lkreidberg/batman/tutorial.html#limb-darkening-options

    exp_time_minutes : float
        The amount of time to 'smear' the transit LC points over to simulate a
        long exposure time.

    supersample_factor: int
        The number of supersampled time data points to average the lightcurve
        model over.

    Returns
    -------

    (params, batman_model) : tuple
        The returned tuple contains the params list and the generated
        `batman.TransitModel` object.

    '''
    params = batman.TransitParams()  # object to store transit parameters
    params.t0 = t0                   # time of periastron
    params.per = per                 # orbital period
    params.rp = rp                   # planet radius (in stellar radii)
    params.a = a                     # semi-major axis (in stellar radii)
    params.inc = inc                 # orbital inclination (in degrees)
    params.ecc = ecc                 # the eccentricity of the orbit
    params.w = w                     # longitude of periastron (in degrees)
    params.u = u                     # limb darkening coefficient list
    params.limb_dark = limb_dark     # limb darkening model to use

    t = times
    m = batman.TransitModel(params, t, exp_time=exp_time_minutes/60./24.,
                            supersample_factor=supersample_factor)

    return params, m