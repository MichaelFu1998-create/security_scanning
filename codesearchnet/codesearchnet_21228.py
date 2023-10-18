def teff(cluster):
    """
    Calculate Teff for main sequence stars ranging from Teff 3500K - 8000K. Use
    [Fe/H] of the cluster, if available.

    Returns a list of Teff values.
    """
    b_vs, _ = cluster.stars()
    teffs = []
    for b_v in b_vs:
        b_v -= cluster.eb_v
        if b_v > -0.04:
            x = (14.551 - b_v) / 3.684
        else:
            x = (3.402 - math.sqrt(0.515 + 1.376 * b_v)) / 0.688

        teffs.append(math.pow(10, x))
    return teffs