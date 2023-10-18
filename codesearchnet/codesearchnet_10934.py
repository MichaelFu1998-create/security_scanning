def populations_diff_coeff(particles, populations):
    """Diffusion coefficients of the two specified populations.
    """
    D_counts = particles.diffusion_coeff_counts
    if len(D_counts) == 1:
        pop_sizes = [pop.stop - pop.start for pop in populations]
        assert D_counts[0][1] >= sum(pop_sizes)
        D_counts = [(D_counts[0][0], ps) for ps in pop_sizes]

    D_list = []
    D_pop_start = 0  # start index of diffusion-based populations
    for pop, (D, counts) in zip(populations, D_counts):
        D_list.append(D)
        assert pop.start >= D_pop_start
        assert pop.stop <= D_pop_start + counts
        D_pop_start += counts
    return D_list