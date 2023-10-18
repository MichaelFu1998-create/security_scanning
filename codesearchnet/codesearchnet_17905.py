def dorun(SNR=20, njitters=20, samples=10, noise_samples=10, sweeps=20, burn=10):
    """
    we want to display the errors introduced by pixelation so we plot:
        * CRB, sampled error vs exposure time

    a = dorun(ntimes=10, samples=5, noise_samples=5, sweeps=20, burn=8)
    """
    jitters = np.logspace(-6, np.log10(0.5), njitters)
    crbs, vals, errs, poss = [], [], [], []

    for i,t in enumerate(jitters):
        print '###### jitter', i, t

        for j in xrange(samples):
            print 'image', j, '|', 
            s,im,pos = zjitter(jitter=t)

            # typical image
            common.set_image(s, im, 1.0/SNR)
            crbs.append(crb(s))

            val, err = sample(s, im, 1.0/SNR, N=noise_samples, sweeps=sweeps, burn=burn)
            poss.append(pos)
            vals.append(val)
            errs.append(err)


    shape0 = (njitters, samples, -1)
    shape1 = (njitters, samples, noise_samples, -1)

    crbs = np.array(crbs).reshape(shape0)
    vals = np.array(vals).reshape(shape1)
    errs = np.array(errs).reshape(shape1)
    poss = np.array(poss).reshape(shape0)

    return  [crbs, vals, errs, poss, jitters]