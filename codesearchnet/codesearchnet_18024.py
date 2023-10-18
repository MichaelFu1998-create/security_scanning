def do_levmarq_all_particle_groups(s, region_size=40, max_iter=2, damping=1.0,
        decrease_damp_factor=10., run_length=4, collect_stats=False, **kwargs):
    """
    Levenberg-Marquardt optimization for every particle in the state.

    Convenience wrapper for LMParticleGroupCollection. Same keyword args,
    but I've set the defaults to what I've found to be useful values for
    optimizing particles. See LMParticleGroupCollection for documentation.

    See Also
    --------
        do_levmarq_particles : Levenberg-Marquardt optimization of a
            specified set of particles.

        do_levmarq : Levenberg-Marquardt optimization of the entire state;
            useful for optimizing global parameters.

        LMParticleGroupCollection : The workhorse of do_levmarq.

        LMEngine : Engine superclass for all the optimizers.
    """
    lp = LMParticleGroupCollection(s, region_size=region_size, damping=damping,
            run_length=run_length, decrease_damp_factor=decrease_damp_factor,
            get_cos=collect_stats, max_iter=max_iter, **kwargs)
    lp.do_run_2()
    if collect_stats:
        return lp.stats