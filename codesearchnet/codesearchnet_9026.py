def do_chan_log_normal(self, line):
        """Set the channel log level to NORMAL. Command syntax is: chan_log_normal"""
        self.application.channel.SetLogFilters(openpal.LogFilters(opendnp3.levels.NORMAL))
        print('Channel log filtering level is now: {0}'.format(opendnp3.levels.NORMAL))