def thread_check(nthreads=3):
    """
    Start a number of threads and verify each has a unique Octave session.

    Parameters
    ==========
    nthreads : int
        Number of threads to use.

    Raises
    ======
    Oct2PyError
        If the thread does not sucessfully demonstrate independence.

    """
    print("Starting {0} threads at {1}".format(nthreads,
                                               datetime.datetime.now()))
    threads = []
    for i in range(nthreads):
        thread = ThreadClass()
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('All threads closed at {0}'.format(datetime.datetime.now()))