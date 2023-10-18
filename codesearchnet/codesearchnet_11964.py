def find_lc_timegroups(lctimes, mingap=4.0):
    '''Finds gaps in the provided time-series and indexes them into groups.

    This finds the gaps in the provided `lctimes` array, so we can figure out
    which times are for consecutive observations and which represent gaps
    between seasons or observing eras.

    Parameters
    ----------

    lctimes : array-like
        This contains the times to analyze for gaps; assumed to be some form of
        Julian date.

    mingap : float
        This defines how much the difference between consecutive measurements is
        allowed to be to consider them as parts of different timegroups. By
        default it is set to 4.0 days.

    Returns
    -------

    tuple
        A tuple of the form: `(ngroups, [slice(start_ind_1, end_ind_1), ...])`
        is returned.  This contains the number of groups as the first element,
        and a list of Python `slice` objects for each time-group found. These
        can be used directly to index into the array of times to quickly get
        measurements associated with each group.

    '''

    lc_time_diffs = np.diff(lctimes)
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