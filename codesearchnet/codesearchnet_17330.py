def startprocessmonitor(self, process_name, interval=2):
        """
        Start memory and CPU monitoring, with the time interval between
        each process scan

        @param process_name: Process name, ex: firefox-bin.
        @type process_name: string
        @param interval: Time interval between each process scan
        @type interval: double

        @return: 1 on success
        @rtype: integer
        """
        if process_name in self._process_stats:
            # Stop previously running instance
            # At any point, only one process name can be tracked
            # If an instance already exist, then stop it
            self._process_stats[process_name].stop()
        # Create an instance of process stat
        self._process_stats[process_name] = ProcessStats(process_name, interval)
        # start monitoring the process
        self._process_stats[process_name].start()
        return 1