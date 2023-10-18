def find_lc_timegroups(lctimes, mingap=4.0):
    '''This finds the time gaps in the light curve, so we can figure out which
    times are for consecutive observations and which represent gaps
    between seasons.

    Parameters
    ----------

    lctimes : np.array
        This is the input array of times, assumed to be in some form of JD.

    mingap : float
        This defines how much the difference between consecutive measurements is
        allowed to be to consider them as parts of different timegroups. By
        default it is set to 4.0 days.

    Returns
    -------

    tuple
        A tuple of the form below is returned, containing the number of time
        groups found and Python slice objects for each group::

            (ngroups, [slice(start_ind_1, end_ind_1), ...])

    '''

    lc_time_diffs = [(lctimes[x] - lctimes[x-1]) for x in range(1,len(lctimes))]
    lc_time_diffs = np.array(lc_time_diffs)

    group_start_indices = np.where(lc_time_diffs > mingap)[0]

    if len(group_start_indices) > 0:

        group_indices = []

        for i, gindex in enumerate(group_start_indices):

            if i == 0:
                group_indices.append(slice(0,gindex+1))
            else:
                group_indices.append(slice(group_start_indices[i-1]+1,gindex+1))


        # at the end, add the slice for the last group to the end of the times
        # array
        group_indices.append(slice(group_start_indices[-1]+1,len(lctimes)))

    # if there's no large gap in the LC, then there's only one group to worry
    # about
    else:
        group_indices = [slice(0,len(lctimes))]


    return len(group_indices), group_indices