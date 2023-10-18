def do_mast_log_normal(self, line):
        """Set the master log level to NORMAL. Command syntax is: mast_log_normal"""
        self.application.master.SetLogFilters(openpal.LogFilters(opendnp3.levels.NORMAL))
        _log.debug('Master log filtering level is now: {0}'.format(opendnp3.levels.NORMAL))