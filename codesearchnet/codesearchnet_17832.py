def _feature_guess(im, rad, minmass=None, use_tp=False, trim_edge=False):
    """Workhorse of feature_guess"""
    if minmass is None:
        # we use 1% of the feature size mass as a cutoff;
        # it's easier to remove than to add
        minmass = rad**3 * 4/3.*np.pi * 0.01
        # 0.03 is a magic number; works well
    if use_tp:
        diameter = np.ceil(2*rad)
        diameter += 1-(diameter % 2)
        df = peri.trackpy.locate(im, int(diameter), minmass=minmass)
        npart = np.array(df['mass']).size
        guess = np.zeros([npart, 3])
        guess[:, 0] = df['z']
        guess[:, 1] = df['y']
        guess[:, 2] = df['x']
        mass = df['mass']
    else:
        guess, mass = initializers.local_max_featuring(
            im, radius=rad, minmass=minmass, trim_edge=trim_edge)
        npart = guess.shape[0]
    # I want to return these sorted by mass:
    inds = np.argsort(mass)[::-1]  # biggest mass first
    return guess[inds].copy(), npart