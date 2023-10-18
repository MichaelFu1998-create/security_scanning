def parallel_gen_timestamps(dview, max_em_rate, bg_rate):
    """Generate timestamps from a set of remote simulations in `dview`.
    Assumes that all the engines have an `S` object already containing
    an emission trace (`S.em`). The "photons" timestamps are generated
    from these emission traces and merged into a single array of timestamps.
    `max_em_rate` and `bg_rate` are passed to `S.sim_timetrace()`.
    """
    dview.execute('S.sim_timestamps_em_store(max_rate=%d, bg_rate=%d, '
                  'seed=S.EID, overwrite=True)' % (max_em_rate, bg_rate))
    dview.execute('times = S.timestamps[:]')
    dview.execute('times_par = S.timestamps_par[:]')
    Times = dview['times']
    Times_par = dview['times_par']
    # Assuming all t_max equal, just take the first
    t_max = dview['S.t_max'][0]
    t_tot = np.sum(dview['S.t_max'])
    dview.execute("sim_name = S.compact_name_core(t_max=False, hashdigit=0)")
    # Core names contains no ID or t_max
    sim_name = dview['sim_name'][0]
    times_all, times_par_all = merge_ph_times(Times, Times_par,
                                              time_block=t_max)
    return times_all, times_par_all, t_tot, sim_name