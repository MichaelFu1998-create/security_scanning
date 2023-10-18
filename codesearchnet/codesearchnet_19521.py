def tictoc(name='tictoc'):
    """
    with tictoc('any string or not'):
        print 'cool~~~'
    cool~~~
    2015-12-30 14:39:28,458 [INFO] tictoc Elapsed: 7.10487365723e-05 secs
    :param name: str
    """
    t = time.time()
    yield
    logg.info('%s Elapsed: %s secs' % (name, time.time() - t))