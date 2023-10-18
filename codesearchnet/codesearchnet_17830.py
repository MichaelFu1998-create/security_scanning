def dorun(SNR=20, ntimes=20, samples=10, noise_samples=10, sweeps=20, burn=10,
        correlated=False):
    """
    we want to display the errors introduced by pixelation so we plot:
        * CRB, sampled error vs exposure time

    a = dorun(ntimes=10, samples=5, noise_samples=5, sweeps=20, burn=8)
    """
    if not correlated:
        times = np.logspace(-3, 0, ntimes)
    else:
        times = np.logspace(np.log10(0.05), np.log10(30), ntimes)

    crbs, vals, errs, poss = [], [], [], []

    for i,t in enumerate(times):
        print '###### time', i, t

        for j in xrange(samples):
            print 'image', j, '|', 
            if not correlated:
                s,im,pos = diffusion(diffusion_constant=0.2, exposure_time=t)
            else:
                s,im,pos = diffusion_correlated(diffusion_constant=0.2, exposure_time=t)

            # typical image
            common.set_image(s, im, 1.0/SNR)
            crbs.append(common.crb(s))

            val, err = common.sample(s, im, 1.0/SNR, N=noise_samples, sweeps=sweeps, burn=burn)
            poss.append(pos)
            vals.append(val)
            errs.append(err)


    shape0 = (ntimes, samples, -1)
    shape1 = (ntimes, samples, noise_samples, -1)

    crbs = np.array(crbs).reshape(shape0)
    vals = np.array(vals).reshape(shape1)
    errs = np.array(errs).reshape(shape1)
    poss = np.array(poss).reshape(shape0)

    return  [crbs, vals, errs, poss, times]