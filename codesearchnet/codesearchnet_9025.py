def do_chan_log_all(self, line):
        """Set the channel log level to ALL_COMMS. Command syntax is: chan_log_all"""
        self.application.channel.SetLogFilters(openpal.LogFilters(opendnp3.levels.ALL_COMMS))
        print('Channel log filtering level is now: {0}'.format(opendnp3.levels.ALL_COMMS))