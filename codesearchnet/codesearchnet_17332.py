def getcpustat(self, process_name):
        """
        get CPU stat for the give process name

        @param process_name: Process name, ex: firefox-bin.
        @type process_name: string

        @return: cpu stat list on success, else empty list
                If same process name, running multiple instance,
                get the stat of all the process CPU usage
        @rtype: list
        """
        # Create an instance of process stat
        _stat_inst = ProcessStats(process_name)
        _stat_list = []
        for p in _stat_inst.get_cpu_memory_stat():
            try:
                _stat_list.append(p.get_cpu_percent())
            except psutil.AccessDenied:
                pass
        return _stat_list