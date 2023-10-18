def diffusion_correlated(diffusion_constant=0.2, exposure_time=0.05,
        samples=40, phi=0.25):
    """
    Calculate the (perhaps) correlated diffusion effect between particles
    during the exposure time of the confocal microscope. diffusion_constant is
    in terms of seconds and pixel sizes exposure_time is in seconds

    1 micron radius particle:
        D = kT / (6 a\pi\eta)
        for 80/20 g/w (60 mPas), 3600 nm^2/sec ~ 0.15 px^2/sec
        for 100 % w  (0.9 mPas),               ~ 10.1 px^2/sec
    a full 60 layer scan takes 0.1 sec, so a particle is 0.016 sec exposure
    """
    radius = 5
    psfsize = np.array([2.0, 1.0, 3.0])/2

    pos, rad, tile = nbody.initialize_particles(N=50, phi=phi, polydispersity=0.0)
    sim = nbody.BrownianHardSphereSimulation(
        pos, rad, tile, D=diffusion_constant, dt=exposure_time/samples
    )
    sim.dt = 1e-2
    sim.relax(2000)
    sim.dt = exposure_time/samples

    # move the center to index 0 for easier analysis later
    c = ((sim.pos - sim.tile.center())**2).sum(axis=-1).argmin()
    pc = sim.pos[c].copy()
    sim.pos[c] = sim.pos[0]
    sim.pos[0] = pc

    # which particles do we want to simulate motion for? particle
    # zero and its neighbors
    mask = np.zeros_like(sim.rad).astype('bool')
    neigh = sim.neighbors(3*radius, 0)
    for i in neigh+[0]:
        mask[i] = True

    img = np.zeros(sim.tile.shape)
    s0 = runner.create_state(img, sim.pos, sim.rad, ignoreimage=True)

    # add up a bunch of trajectories
    finalimage = 0*s0.get_model_image()[s0.inner]
    position = 0*s0.obj.pos

    for i in xrange(samples):
        sim.step(1, mask=mask)
        s0.obj.pos = sim.pos.copy() + s0.pad
        s0.reset()

        finalimage += s0.get_model_image()[s0.inner]
        position += s0.obj.pos

    finalimage /= float(samples)
    position /= float(samples)

    # place that into a new image at the expected parameters
    s = runner.create_state(img, sim.pos, sim.rad, ignoreimage=True)
    s.reset()

    # measure the true inferred parameters
    return s, finalimage, position