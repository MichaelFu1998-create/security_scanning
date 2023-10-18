def _parallel_bls_worker(task):
    '''
    This wraps the BLS function for the parallel driver below.

    Parameters
    ----------

    tasks : tuple
        This is of the form::

            task[0] = times
            task[1] = mags
            task[2] = nfreq
            task[3] = freqmin
            task[4] = stepsize
            task[5] = nbins
            task[6] = minduration
            task[7] = maxduration

    Returns
    -------

    dict
        Returns a dict of the form::

            {
                'power':           the periodogram power array,
                'bestperiod':      the best period found,
                'bestpower':       the highest peak of the periodogram power,
                'transdepth':      transit depth found by eebls.f,
                'transduration':   transit duration found by eebls.f,
                'transingressbin': transit ingress bin found by eebls.f,
                'transegressbin':  transit egress bin found by eebls.f,
            }

    '''

    try:

        return _bls_runner(*task)

    except Exception as e:

        LOGEXCEPTION('BLS failed for task %s' % repr(task[2:]))

        return {
            'power':nparray([npnan for x in range(task[2])]),
            'bestperiod':npnan,
            'bestpower':npnan,
            'transdepth':npnan,
            'transduration':npnan,
            'transingressbin':npnan,
            'transegressbin':npnan
        }