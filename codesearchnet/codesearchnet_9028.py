def do_mast_log_all(self, line):
        """Set the master log level to ALL_COMMS. Command syntax is: mast_log_all"""
        self.application.master.SetLogFilters(openpal.LogFilters(opendnp3.levels.ALL_COMMS))
        _log.debug('Master log filtering level is now: {0}'.format(opendnp3.levels.ALL_COMMS))