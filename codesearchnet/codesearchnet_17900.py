def dorun(SNR=20, sweeps=20, burn=8, noise_samples=10):
    """
    we want to display the errors introduced by pixelation so we plot:
        * zero noise, cg image, fit
        * SNR 20, cg image, fit
        * CRB for both

    a = dorun(noise_samples=30, sweeps=24, burn=12, SNR=20)
    """
    radii = np.linspace(2,10,8, endpoint=False)
    crbs, vals, errs = [], [], []

    for radius in radii:
        print 'radius', radius
        s,im = pxint(radius=radius, factor=4)
        goodstate = s.state.copy()

        common.set_image(s, im, 1.0/SNR)
        tcrb = crb(s)
        tval, terr = sample(s, im, 1.0/SNR, N=noise_samples, sweeps=sweeps, burn=burn)
        crbs.append(tcrb)
        vals.append(tval)
        errs.append(terr)

    return np.array(crbs), np.array(vals), np.array(errs), radii