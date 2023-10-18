def do_levmarq_particles(s, particles, damping=1.0, decrease_damp_factor=10.,
        run_length=4, collect_stats=False, max_iter=2, **kwargs):
    """
    Levenberg-Marquardt optimization on a set of particles.

    Convenience wrapper for LMParticles. Same keyword args, but the
    defaults have been set to useful values for optimizing particles.
    See LMParticles and LMEngine for documentation.

    See Also
    --------
        do_levmarq_all_particle_groups : Levenberg-Marquardt optimization
            of all the particles in the state.

        do_levmarq : Levenberg-Marquardt optimization of the entire state;
            useful for optimizing global parameters.

        LMParticles : Optimizer object; the workhorse of do_levmarq_particles.

        LMEngine : Engine superclass for all the optimizers.
    """
    lp = LMParticles(s, particles, damping=damping, run_length=run_length,
            decrease_damp_factor=decrease_damp_factor, max_iter=max_iter,
            **kwargs)
    lp.do_run_2()
    if collect_stats:
        return lp.get_termination_stats()