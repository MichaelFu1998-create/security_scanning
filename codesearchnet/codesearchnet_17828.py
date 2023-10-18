def diffusion(diffusion_constant=0.2, exposure_time=0.05, samples=200):
    """
    See `diffusion_correlated` for information related to units, etc
    """
    radius = 5
    psfsize = np.array([2.0, 1.0, 3.0])

    # create a base image of one particle
    s0 = init.create_single_particle_state(imsize=4*radius, 
            radius=radius, psfargs={'params': psfsize, 'error': 1e-6})

    # add up a bunch of trajectories
    finalimage = 0*s0.get_model_image()[s0.inner]
    position = 0*s0.obj.pos[0]

    for i in xrange(samples):
        offset = np.sqrt(6*diffusion_constant*exposure_time)*np.random.randn(3)
        s0.obj.pos[0] = np.array(s0.image.shape)/2 + offset
        s0.reset()

        finalimage += s0.get_model_image()[s0.inner]
        position += s0.obj.pos[0]

    finalimage /= float(samples)
    position /= float(samples)

    # place that into a new image at the expected parameters
    s = init.create_single_particle_state(imsize=4*radius, sigma=0.05,
            radius=radius, psfargs={'params': psfsize, 'error': 1e-6})
    s.reset()

    # measure the true inferred parameters
    return s, finalimage, position