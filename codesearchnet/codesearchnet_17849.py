def dorun(method, platonics=None, nsnrs=20, noise_samples=30, sweeps=30, burn=15):
    """
    platonics = create_many_platonics(N=50)
    dorun(platonics)
    """
    sigmas = np.logspace(np.log10(1.0/2048), 0, nsnrs)
    crbs, vals, errs, poss = [], [], [], []

    for sigma in sigmas:
        print "#### sigma:", sigma

        for i, (image, pos) in enumerate(platonics):
            print 'image', i, '|', 
            s,im = create_comparison_state(image, pos, method=method)

            # typical image
            set_image(s, im, sigma)
            crbs.append(crb(s))

            val, err = sample(s, im, sigma, N=noise_samples, sweeps=sweeps, burn=burn)
            poss.append(pos)
            vals.append(val)
            errs.append(err)


    shape0 = (nsnrs, len(platonics), -1)
    shape1 = (nsnrs, len(platonics), noise_samples, -1)

    crbs = np.array(crbs).reshape(shape0)
    vals = np.array(vals).reshape(shape1)
    errs = np.array(errs).reshape(shape1)
    poss = np.array(poss).reshape(shape0)

    return  [crbs, vals, errs, poss, sigmas]