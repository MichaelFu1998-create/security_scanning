def merge_ph_times(times_list, times_par_list, time_block):
    """Build an array of timestamps joining the arrays in `ph_times_list`.
    `time_block` is the duration of each array of timestamps.
    """
    offsets = np.arange(len(times_list)) * time_block
    cum_sizes = np.cumsum([ts.size for ts in times_list])
    times = np.zeros(cum_sizes[-1])
    times_par = np.zeros(cum_sizes[-1], dtype='uint8')
    i1 = 0
    for i2, ts, ts_par, offset in zip(cum_sizes, times_list, times_par_list,
                                      offsets):
        times[i1:i2] = ts + offset
        times_par[i1:i2] = ts_par
        i1 = i2
    return times, times_par