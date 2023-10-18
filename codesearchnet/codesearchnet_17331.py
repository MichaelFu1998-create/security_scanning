def stopprocessmonitor(self, process_name):
        """
        Stop memory and CPU monitoring

        @param process_name: Process name, ex: firefox-bin.
        @type process_name: string

        @return: 1 on success
        @rtype: integer
        """
        if process_name in self._process_stats:
            # Stop monitoring process
            self._process_stats[process_name].stop()
        return 1