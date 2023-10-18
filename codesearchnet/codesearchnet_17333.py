def getmemorystat(self, process_name):
        """
        get memory stat

        @param process_name: Process name, ex: firefox-bin.
        @type process_name: string

        @return: memory stat list on success, else empty list
                If same process name, running multiple instance,
                get the stat of all the process memory usage
        @rtype: list
        """
        # Create an instance of process stat
        _stat_inst = ProcessStats(process_name)
        _stat_list = []
        for p in _stat_inst.get_cpu_memory_stat():
            # Memory percent returned with 17 decimal values
            # ex: 0.16908645629882812, round it to 2 decimal values
            # as 0.03
            try:
                _stat_list.append(round(p.get_memory_percent(), 2))
            except psutil.AccessDenied:
                pass
        return _stat_list