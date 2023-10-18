def fit_edge(separation, radius=5.0, samples=100, imsize=64, sigma=0.05, axis='z'):
    """
    axis is 'z' or 'xy'
    seps = np.linspace(0,2,20) 'z'
    seps = np.linspace(-2,2,20) 'xy'
    """
    terrors = []
    berrors = []
    crbs = []

    for sep in separation:
        print '='*79
        print 'sep =', sep,

        s = init.create_two_particle_state(imsize, radius=radius, delta=sep, sigma=0.05,
                axis='z', psfargs={'params': (2.0,1.0,4.0), 'error': 1e-8},
                          stateargs={'sigmapad': True, 'pad': const.PAD})

        # move off of a pixel edge (cheating for trackpy)
        d = np.array([0,0.5,0.5])
        s.obj.pos -= d
        s.reset()

        # move the particles to the edge
        bl = s.blocks_particle(0)
        s.update(bl[0], np.array([s.pad+radius]))

        bl = s.blocks_particle(1)
        s.update(bl[0], np.array([s.pad-radius]))

        if axis == 'z':
            bl = s.blocks_particle(1)
            s.update(bl[0], s.state[bl[0]]-sep)
            s.model_to_true_image()

        if axis == 'xy':
            bl = s.blocks_particle(1)
            s.update(bl[2], s.state[bl[2]]+sep)
            s.model_to_true_image()

        # save where the particles were originally so we can jiggle
        p = s.state[s.b_pos].reshape(-1,3).copy()

        print p[0], p[1]
        # calculate the CRB for this configuration
        bl = s.explode(s.b_pos)
        crbs.append(np.sqrt(np.diag(np.linalg.inv(s.fisher_information(blocks=bl)))).reshape(-1,3))

        # calculate the featuring errors
        tmp_tp, tmp_bf = [],[]
        for i in xrange(samples):
            print i
            bench.jiggle_particles(s, pos=p, sig=0.3, mask=np.array([1,1,1]))
            t = bench.trackpy(s)
            b = bench.bamfpy_positions(s, sweeps=15)

            tmp_tp.append(bench.error(s, t))
            tmp_bf.append(bench.error(s, b))
        terrors.append(tmp_tp)
        berrors.append(tmp_bf)

    return np.array(crbs), np.array(terrors), np.array(berrors)