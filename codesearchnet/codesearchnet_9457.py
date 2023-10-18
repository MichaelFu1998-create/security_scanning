def register_memory():
    """Register an approximation of memory used by FTP server process
    and all of its children.
    """
    # XXX How to get a reliable representation of memory being used is
    # not clear. (rss - shared) seems kind of ok but we might also use
    # the private working set via get_memory_maps().private*.
    def get_mem(proc):
        if os.name == 'posix':
            mem = proc.memory_info_ex()
            counter = mem.rss
            if 'shared' in mem._fields:
                counter -= mem.shared
            return counter
        else:
            # TODO figure out what to do on Windows
            return proc.get_memory_info().rss

    if SERVER_PROC is not None:
        mem = get_mem(SERVER_PROC)
        for child in SERVER_PROC.children():
            mem += get_mem(child)
        server_memory.append(bytes2human(mem))