def cpu_count():
    """ Returns the default number of slave processes to be spawned.

        The default value is the number of physical cpu cores seen by python.
        :code:`OMP_NUM_THREADS` environment variable overrides it.

        On PBS/torque systems if OMP_NUM_THREADS is empty, we try to
        use the value of :code:`PBS_NUM_PPN` variable.

        Notes
        -----
        On some machines the physical number of cores does not equal
        the number of cpus shall be used. PSC Blacklight for example.

    """
    num = os.getenv("OMP_NUM_THREADS")
    if num is None:
        num = os.getenv("PBS_NUM_PPN")
    try:
        return int(num)
    except:
        return multiprocessing.cpu_count()