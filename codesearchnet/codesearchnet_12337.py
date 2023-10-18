def _cpinfo_key_worker(task):
    '''This wraps `checkplotlist.checkplot_infokey_worker`.

    This is used to get the correct dtype for each element in retrieved results.

    Parameters
    ----------

    task : tuple
        task[0] = cpfile
        task[1] = keyspeclist (infokeys kwarg from `add_cpinfo_to_lclist`)

    Returns
    -------

    dict
        All of the requested keys from the checkplot are returned along with
        their values in a dict.

    '''

    cpfile, keyspeclist = task

    keystoget = [x[0] for x in keyspeclist]
    nonesubs = [x[-2] for x in keyspeclist]
    nansubs = [x[-1] for x in keyspeclist]

    # reform the keystoget into a list of lists
    for i, k in enumerate(keystoget):

        thisk = k.split('.')
        if sys.version_info[:2] < (3,4):
            thisk = [(int(x) if x.isdigit() else x) for x in thisk]
        else:
            thisk = [(int(x) if x.isdecimal() else x) for x in thisk]

        keystoget[i] = thisk

    # add in the objectid as well to match to the object catalog later
    keystoget.insert(0,['objectid'])
    nonesubs.insert(0, '')
    nansubs.insert(0,'')

    # get all the keys we need
    vals = checkplot_infokey_worker((cpfile, keystoget))

    # if they have some Nones, nans, etc., reform them as expected
    for val, nonesub, nansub, valind in zip(vals, nonesubs,
                                            nansubs, range(len(vals))):

        if val is None:
            outval = nonesub
        elif isinstance(val, float) and not np.isfinite(val):
            outval = nansub
        elif isinstance(val, (list, tuple)):
            outval = ', '.join(val)
        else:
            outval = val

        vals[valind] = outval

    return vals