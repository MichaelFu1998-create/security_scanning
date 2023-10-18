def merge_particle_emission(SS):
    """Returns a sim object summing the emissions and particles in SS (list).
    """
    # Merge all the particles
    P = reduce(lambda x, y: x + y, [Si.particles for Si in SS])
    s = SS[0]
    S = ParticlesSimulation(t_step=s.t_step, t_max=s.t_max,
                            particles=P, box=s.box, psf=s.psf)
    S.em = np.zeros(s.em.shape, dtype=np.float64)
    for Si in SS:
        S.em += Si.em
    return S