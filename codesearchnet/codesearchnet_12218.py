def read_hatpi_pklc(lcfile):
    '''
    This just reads a pickle LC. Returns an lcdict.

    '''

    try:

        if lcfile.endswith('.gz'):
            infd = gzip.open(lcfile,'rb')
        else:
            infd = open(lcfile,'rb')

        lcdict = pickle.load(infd)
        infd.close()

        return lcdict

    except UnicodeDecodeError:

        if lcfile.endswith('.gz'):
            infd = gzip.open(lcfile,'rb')
        else:
            infd = open(lcfile,'rb')

        LOGWARNING('pickle %s was probably from Python 2 '
                   'and failed to load without using "latin1" encoding. '
                   'This is probably a numpy issue: '
                   'http://stackoverflow.com/q/11305790' % lcfile)
        lcdict = pickle.load(infd, encoding='latin1')
        infd.close()

        return lcdict