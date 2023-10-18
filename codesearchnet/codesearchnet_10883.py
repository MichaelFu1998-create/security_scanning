def merge_DA_ph_times(ph_times_d, ph_times_a):
    """Returns a merged timestamp array for Donor+Accept. and bool mask for A.
    """
    ph_times = np.hstack([ph_times_d, ph_times_a])
    a_em = np.hstack([np.zeros(ph_times_d.size, dtype=np.bool),
                      np.ones(ph_times_a.size, dtype=np.bool)])
    index_sort = ph_times.argsort()
    return ph_times[index_sort], a_em[index_sort]