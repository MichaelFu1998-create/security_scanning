def load_wisdom(wisdomfile):
    """
    Prime FFTW with knowledge of which FFTs are best on this machine by
    loading 'wisdom' from the file ``wisdomfile``
    """
    if wisdomfile is None:
        return

    try:
        pyfftw.import_wisdom(pickle.load(open(wisdomfile, 'rb')))
    except (IOError, TypeError) as e:
        log.warn("No wisdom present, generating some at %r" % wisdomfile)
        save_wisdom(wisdomfile)