def missing_particle(separation=0.0, radius=RADIUS, SNR=20):
    """ create a two particle state and compare it to featuring using a single particle guess """
    # create a base image of one particle
    s = init.create_two_particle_state(imsize=6*radius+4, axis='x', sigma=1.0/SNR,
            delta=separation, radius=radius, stateargs={'varyn': True}, psfargs={'error': 1e-6})
    s.obj.typ[1] = 0.
    s.reset()

    return s, s.obj.pos.copy()