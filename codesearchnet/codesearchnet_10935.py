def populations_slices(particles, num_pop_list):
    """2-tuple of slices for selection of two populations.
    """
    slices = []
    i_prev = 0
    for num_pop in num_pop_list:
        slices.append(slice(i_prev, i_prev + num_pop))
        i_prev += num_pop
    return slices