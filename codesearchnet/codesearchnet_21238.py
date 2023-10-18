def round_teff_luminosity(cluster):
    """
    Returns rounded teff and luminosity lists.
    """
    temps = [round(t, -1) for t in teff(cluster)]
    lums = [round(l, 3) for l in luminosity(cluster)]
    return temps, lums