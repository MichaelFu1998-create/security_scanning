def total_memory():
    """ Returns the the amount of memory available for use.

        The memory is obtained from MemTotal entry in /proc/meminfo.
        
        Notes
        =====
        This function is not very useful and not very portable. 

    """
    with file('/proc/meminfo', 'r') as f:
        for line in f:
            words = line.split()
        if words[0].upper() == 'MEMTOTAL:':
            return int(words[1]) * 1024
    raise IOError('MemTotal unknown')